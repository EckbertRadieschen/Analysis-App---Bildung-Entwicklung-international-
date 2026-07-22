import streamlit as st

def intro_page():
    with st.container(key="intro_container"):
        st.markdown("""
            ### Bildung als Faktor gesellschaftlicher Entwicklung

            Bildung gilt als einer der wichtigsten Einflussfaktoren für die langfristige gesellschaftliche 
            und wirtschaftliche Entwicklung eines Landes.<br>
            Doch lässt sich dieser Zusammenhang auch anhand internationaler Daten nachweisen?

            Diese Anwendung ermöglicht eine **explorative Datenanalyse**, bei der Bildungsindikatoren mit 
            verschiedenen Entwicklungsindikatoren aus den Bereichen

            - Wirtschaft, Staat & Institutionen, Gesellschaft
            - Gesundheit, Umwelt
            - Technologie, Innovation

            verglichen werden.

            Die Datengrundlage basiert auf internationalen Datensätzen der World Bank of Data und ermöglicht es,<br>
            Zusammenhänge zwischen Bildungsleistungen und Entwicklungskennzahlen verschiedener Länder zu untersuchen.

            > **Hinweis:** Die dargestellten Ergebnisse zeigen statistische Zusammenhänge (**Korrelationen**) 
            und dienen der Exploration der Daten.<br>
            Sie erlauben **keine Aussagen über Ursache und Wirkung (Kausalität)**,<br>
            da gesellschaftliche Entwicklung von zahlreichen miteinander verknüpften Faktoren beeinflusst wird.

            #### So verwenden Sie die Anwendung

            1. Wählen Sie einen **Bildungsindikator** aus.
            2. Wählen Sie anschließend eine **Entwicklungsvariable**.
            3. Analysieren Sie die Beziehung zwischen beiden Variablen anhand verschiedener Visualisierungen und statistischer Kennzahlen.

            Viel Freude beim Entdecken spannender Zusammenhänge zwischen **Bildung** und **gesellschaftlicher Entwicklung**!
            """,
            unsafe_allow_html=True
        )
