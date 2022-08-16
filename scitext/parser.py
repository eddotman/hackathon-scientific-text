import cohere
import pubchempy as pcp


class Parser:
    def __init__(self, client: cohere.Client, config: dict = None):

        if not config:
            self.config = {
                "temp_low": 0.1,
                "temp_high": 1,
                "max_tokens": 300,
                "model": "xlarge",
                "rephrase_path": "templates/rephrasing.txt",
                "extract_path": "templates/extraction.txt",
                "summary_path": "templates/summary.txt",
                "stop_seq": "--",
            }
        else:
            self.config = config

        self.co = client
        self.rephrase_prompt = self._load_template(self.config["rephrase_path"])
        self.extract_prompt = self._load_template(self.config["extract_path"])
        self.summary_prompt = self._load_template(self.config["summary_path"])
        self.materials = set()

    def _load_template(self, filepath: str) -> str:
        template_text = ""

        with open(filepath, "r") as f:
            template_text = f.read()

        if not template_text.endswith("\n"):
            template_text += "\n"

        return template_text

    def rephrase(self, text: str) -> str:
        prompt = self.rephrase_prompt + text.rstrip() + "\nRephrasing:"
        response = self.co.generate(
            model=self.config["model"],
            prompt=prompt,
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temp_low"],
            k=0,
            p=0.75,
            stop_sequences=[self.config["stop_seq"]],
        )
        return response.generations[0].text.rstrip(self.config["stop_seq"])

    def extract(self, text: str) -> str:
        prompt = self.extract_prompt + text.rstrip() + "\nMaterials:"
        response = self.co.generate(
            model=self.config["model"],
            prompt=prompt,
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temp_low"],
            k=0,
            p=0.75,
            stop_sequences=[self.config["stop_seq"]],
        )
        generated_text = response.generations[0].text.rstrip(self.config["stop_seq"])
        materials = [m.strip() for m in generated_text.split(",")]

        for material in materials:
            search_results = pcp.get_compounds(material, "name")

            if search_results:
                common_name = search_results[0].synonyms[0].lower()
                smiles = search_results[0].canonical_smiles

                if any(c.isalpha() for c in common_name):
                    self.materials.add(
                        (
                            common_name,
                            smiles,
                        )
                    )

        output_text = ""
        for i, (name, smiles) in enumerate(self.materials):
            output_text += f"{i+1}. {name} ({smiles}) \n"

        return output_text

    def summarize(self, material: str) -> str:
        prompt = self.summary_prompt.rstrip() + " " + material.rstrip() + ":"
        response = self.co.generate(
            model=self.config["model"],
            prompt=prompt,
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temp_high"],
            k=0,
            p=0.75,
            stop_sequences=[self.config["stop_seq"]],
        )
        generated_text = response.generations[0].text.rstrip(self.config["stop_seq"])
        return f"[{material}]" + generated_text + "\n"
