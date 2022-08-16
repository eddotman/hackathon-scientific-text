import os

import cohere
import streamlit as st
from scitext.parser import Parser

parser = Parser(cohere.Client(os.environ.get("COHERE_API_KEY")))


def process_text() -> None:
    if "user_text" in st.session_state:
        if st.session_state["user_text"].strip() != "":

            st.header("Standard Operating Procedure")
            rephrasing = parser.rephrase(st.session_state["user_text"])
            st.write(rephrasing)

            st.header("Common materials detected")
            st.write(parser.extract(rephrasing))

            st.header("Material summaries")
            for material_name, _ in parser.materials:
                st.write(parser.summarize(material_name))


def fill_example_A() -> None:
    if "user_text" in st.session_state:
        st.session_state["user_text"] = (
            "In the experiment procedure, 5.6 µL OAm and 10.4 µL OA were dissolved in 10 mL toluene as solution A, "
            "and x (x = 18.4, 36.8) mg lead iodide (PbI2) and y (y = 12.8, 18.4, 25.6) mg methylammonium iodide were "
            "dissolved in 20 mL acetonitrile as solution B. Then, 2.6 mL solution B was injected into solution A with "
            "different dropping rates under vigorous stirring. The solution turned red at the injection of solution A, "
            "indicating the formation of small-sized perovskite crystals. After stirring for 1 min, 15 mL toluene was "
            "added to the mixed solution dropwise, and kept stirring in the dark for 4 h."
        )


def fill_example_B() -> None:
    if "user_text" in st.session_state:
        st.session_state["user_text"] = (
            "First, layered hydrogen trititanate was prepared via hydrothermal reaction between anatase TiO2 powders and "
            "concentrated NaOH solution at 150 °C for several hours, followed by ion substitution of Na+ with H+ in 0.5 "
            "M HNO3 solution for 3 h. Second, layered LTHs-precursor was obtained by chemical lithiation of hydrogen "
            "trititanate in a 0.8 M LiOH solution heated at 150 °C for 12 h in a Teflon-lined stainless steel autoclave. "
            "Thirdly, a series of lithium titanate hydrates were synthesized by drying the LTHs-precursor at various "
            "temperatures ranging from 80 to 400 °C for 3 h in a vacuum."
        )


if __name__ == "__main__":

    st.set_page_config(
        page_icon="⚛️",
        page_title="Scientific Text Parser",
    )

    st.header("Parse your scientific text! (☞ﾟヮﾟ)☞")

    st.text_area(
        label="Enter some procedure-like scientific text from the **inorganic solid-state materials** domain.",
        key="user_text",
        height=250,
    )

    col1, col2, _, _, _ = st.columns(5)

    with col1:
        st.button(label="Fill Example A", on_click=fill_example_A)

    with col2:
        st.button(
            label="Fill Example B",
            on_click=fill_example_B,
        )

    st.button(
        label="Parse (っ•́｡•́)♪♬",
        on_click=process_text(),
    )
