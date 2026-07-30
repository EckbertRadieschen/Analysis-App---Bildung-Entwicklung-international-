import streamlit as st

def intro_page():
    with st.container(key="intro_container"):
        st.markdown("""
            <div class="custom-title"> Bildung als Faktor gesellschaftlicher Entwicklung</div>
            <div class="small-intro-text">
            Bildung gilt als einer der wichtigsten Einflussfaktoren für die langfristige gesellschaftliche 
            und wirtschaftliche Entwicklung eines Landes.<br>
            Doch lässt sich dieser Zusammenhang auch anhand internationaler Daten nachweisen?<br><br>
            Diese Anwendung ermöglicht eine <b>explorative Datenanalyse</b>, bei der Bildungsindikatoren mit<br> 
            verschiedenen Entwicklungsindikatoren aus den Bereichen<br><br>
            <ul> 
            <li>Wirtschaft, Staat & Institutionen, Gesellschaft</li>
            <li> Gesundheit, Umwelt</li>
            <li> Technologie, Innovation</li>
            </ul>
            verglichen werden.<br><br>
            Die Datengrundlage basiert auf internationalen Datensätzen der World Bank of Data und ermöglicht es,<br>
            Zusammenhänge zwischen Bildungsleistungen und Entwicklungskennzahlen verschiedener Länder zu untersuchen.<br><br>
            <blockquote><b>Hinweis:</b> Die dargestellten Ergebnisse zeigen statistische Zusammenhänge (<b>Korrelationen</b>) 
            und dienen der Exploration der Daten.<br>
            Sie erlauben <b>keine Aussagen über Ursache und Wirkung (Kausalität)</b>,<br>
            da gesellschaftliche Entwicklung von zahlreichen miteinander verknüpften Faktoren beeinflusst wird.</blockquote>
            </div>
            """,
            unsafe_allow_html=True
        )