import glob as g
import streamlit as st
import plotly.graph_objects as go
import pandas as pd



# extraction
def extract_from_csv(file):
    df = pd.read_csv(file, sep=';')
    return df


def extract_data(pathe):
    extracted_data = pd.DataFrame()
    files_csv = g.glob(pathe, recursive=True)
    for i in files_csv:
        extracted_data = extracted_data.append(extract_from_csv(i), ignore_index=True)

        # print( extracted_data.head())

    return extracted_data


def num_et(data):
    Num_etu = data['1. Quel est votre numéro étudiant ? (ex: e22XXXX)'].columns.tolist()
    for i in Num_etu.index:
        Num = Num_etu[i]
        if Num[0].isdigit():
            Num = 'e' + Num[2:]
        Num_etu[i] = Num
    data['1. Quel est votre numéro étudiant ? (ex: e22XXXX)'] = Num_etu
    # print(data['1. Quel est votre numéro étudiant ? (ex: e22XXXX)'])
    return data


# rename columns
column_mapping = {
    '4. Quel est votre degré d\'intérêt pour ces technologies ? (0 → aucun intérêt, 5 → passionné)   [Web (HTML, '
    'CSS , PHP , CMS)]': '4.Web',
    '4. Quel est votre degré d\'intérêt pour ces technologies ? (0 → aucun intérêt, 5 → passionné)   [Cloud (Azure, '
    'AWS,GCP)]': '4.Cloud',
    '4. Quel est votre degré d\'intérêt pour ces technologies ? (0 → aucun intérêt, 5 → passionné)   [Embarqué ('
    'Arduino, Assembleur, Raspberry...)]': '4.Embarqué',
    '4. Quel est votre degré d\'intérêt pour ces technologies ? (0 → aucun intérêt, 5 → passionné)   [Mobile ('
    'Android, iOS,Cross-platform) ]': '4.Mobile',
    '4. Quel est votre degré d\'intérêt pour ces technologies ? (0 → aucun intérêt, 5 → passionné)   [Dev Jeux vidéo '
    '(Unity, Unreal Engine)]': '4.Dev'}


def rename_columns(data, colum):
    data = data.rename(columns=colum)
    return data


def transform_data(data):
    data = num_et(data)
    data = rename_columns(data, column_mapping)
    # print(data)
    return data


# Load data
def load(targetfile, data_to_load):
    data_to_load.to_csv(targetfile)


# execution of ETL (Data pipeline)
path = "/Users/harolddesirebonchouo/Desktop/Astre:Ips/data/data.csv"


def ETL(path):
    extract_df = extract_data(path)
    transform_df = transform_data(data=extract_df)
    transform_df = transform_df.fillna(0)
    load_df = load(targetfile="transformdata1.csv", data_to_load=transform_df)
    return transform_df


New_df = ETL(path)

New_df = New_df.assign(Notes=0)


def switch_example(case):
    if case == 'Ne connais pas':
        note = -1
    elif case == 'Jamais':
        note = 0
    elif case == 'Un peu':
        note = 1
    elif case == 'Régulièrement':
        note = 2
    elif case == 'Tout le temps':
        note = 3
    elif case == 'J\'y suis ':
        note = 2
    elif case == 'Interessé':
        note = 2
    elif case == 'Pas intéressé':
        note = 0
    elif case == 'Prépa intégré':
        note = -1
    elif case == 'CPGE ATS':
        note = 1
    elif case == 'CPGE PT':
        note = 1
    elif case == 'CPGE TSi':
        note = 1
    elif case == 'CPGE MP':
        note = 1
    elif case == 'CPGE MP2I/MPSI':
        note = 1
    elif case == 'CPGE BL':
        note = 1
    elif case == 'CPGE PC':
        note = 1
    elif case == 'BTS SIO':
        note = -1
    elif case == 'BTS SN':
        note = -1
    elif case == 'DUT Informatique':
        note = -1
    elif case == 'DUT Métiers du Multimédia et Internet':
        note = -1
    elif case == 'L2, L3 informatique':
        note = -1
    elif case == 'M1, M2 informatique':
        note = -1
    elif case == 'Windows':
        note = -1
    elif case == 'MacOS':
        note = -1
    elif case == 'Distribution Linux (Ubuntu, Debian, Arch...)':
        note = 1
    elif case == 'C’est un professionnel expert dans un domaine technique capable de résoudre des problèmes de haut ' \
                 'niveau et innovants.':
        note = 1
    elif case == 'Un ingénieur est un Homme capable de prendre du recul et d’avoir une solide culture générale, ' \
                 'technique et humaine.':
        note = -1
    elif case == 'C’est avant tout un cadre supérieur technique qui a pour mission de piloter un projet et de gérer ' \
                 'une ou plusieurs équipes en interface avec le client.':
        note = 1
    else:
        note = 0
    return note


for index, row in New_df.iterrows():
    if row['2. Quelle est la définition d’un ingénieur qui vous correspond le mieux ?']:
        valuer = New_df.at[index, '2. Quelle est la définition d’un ingénieur qui vous correspond le mieux ?']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + switch_example(valuer)

    if row['3. Êtes-vous plutôt programmation ... [Procédurale]']:
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + row[
            '3. Êtes-vous plutôt programmation ... [Procédurale]']
    if row['3. Êtes-vous plutôt programmation ... [Orienté Object]']:
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - row[
            '3. Êtes-vous plutôt programmation ... [Orienté Object]']
    if row['3. Êtes-vous plutôt programmation ... [Fonctionnelle]']:
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + row[
            '3. Êtes-vous plutôt programmation ... [Fonctionnelle]']
    if row['4.Web']:
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - row['4.Web']
    if row['4.Cloud']:
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + row['4.Cloud']
    if row['4.Embarqué']:
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + row['4.Embarqué']
    if row['4.Mobile']:
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - row['4.Mobile']
    if row['4.Dev']:
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - row['4.Dev']
    if row['5. Quelle(s) matière(s) avez-vous aimé particulièrement au lycée parmi les suivantes : ']:
        liste_matiere = New_df.at[
            index, '5. Quelle(s) matière(s) avez-vous aimé particulièrement au lycée parmi les suivantes : '].split(",")
        for matiere in liste_matiere:
            if matiere == 'Maths':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            elif matiere == 'Physique/Chimie':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            elif matiere == 'Littérature/Philosophie':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif matiere == 'Histoire/Géographie':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif matiere == 'Sciences de gestion':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif matiere == 'Arts Plastiques/Arts appliqués':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif matiere == 'Sciences de l\'ingénieur':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            else:
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
    if row['6. Quel(s) cours avez-vous aimé particulièrement au semestre S5 ?']:
        ligne6 = row['6. Quel(s) cours avez-vous aimé particulièrement au semestre S5 ?']
        if ligne6 == "Cryptographie (en Maths)":
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
        elif ligne6 == 'Physique':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
        elif ligne6 == 'Anglais':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
        elif ligne6 == 'Conduite de projet':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
        elif ligne6 == 'Droit du travail':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
        elif ligne6 == 'Electronique':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
        elif ligne6 == 'Programmation informatique':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
        elif ligne6 == 'Technologie de l’internet':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
        elif ligne6 == 'Algorithmique':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
        elif ligne6 == 'Architecture des ordinateurs':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
        elif ligne6 == 'Logique combinatoire et séquentielle':
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
        else:
            New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1

    if (
            row[
                '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [LabView]']):
        valuer = New_df.at[
            index, '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  ' \
                   '[LabView]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + switch_example(valuer)

    if (
            row[
                '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Excel]']):
        valuer = New_df.at[
            index, '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Excel]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - switch_example(valuer)

    if (
            row[
                '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Blender]']):
        valuer = New_df.at[
            index, '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Blender]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - switch_example(valuer)

    if (
            row[
                '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Unity]']):
        valuer = New_df.at[
            index, '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Unity]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - switch_example(valuer)

    if (
            row[
                '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Figma]']):
        valuer = New_df.at[
            index, '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Figma]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - switch_example(valuer)

    if (row[
        '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Cisco Packet Tracer]']):
        valuer = New_df.at[
            index, '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [Cisco Packet Tracer]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + switch_example(valuer)

    if (row[
        '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [SolidWorks]']):
        valuer = New_df.at[
            index, '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [SolidWorks]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + switch_example(valuer)

    if (
            row[
                '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [AutoCAD]']):
        valuer = New_df.at[
            index, '7. Quels logiciels / applications avez-vous l’habitude (ou avez-vous déjà utilisé) d’utiliser ?  [AutoCAD]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + switch_example(valuer)

    if (row['8. Parmi ces machines, lesquelles espérez-vous pouvoir utiliser au cours de vos projets d’année ? ']):
        liste_matiere = New_df.at[
            index, '8. Parmi ces machines, lesquelles espérez-vous pouvoir utiliser au cours de vos projets d’année ? '].split(
            ",")
        for matiere in liste_matiere:
            if (matiere == 'Imprimante 3D'):
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            elif (matiere == 'Drone'):
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            elif (matiere == 'Casque VR'):
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif (matiere == 'Cartes électroniques programmables (Arduino, Raspberry...)'):
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif (matiere == 'Oscilloscope'):
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif (matiere == 'Casque neuronal'):
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            elif (matiere == 'Smartphones'):
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            else:
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1

    if (row['9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [K[art]el]']):
        valuer = New_df.at[
            index, '9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [K[art]el]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - switch_example(valuer)

    if (row['9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [Ensimersion]']):
        valuer = New_df.at[
            index, '9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [Ensimersion]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - switch_example(valuer)

    if (row['9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [Ensim’elec]']):
        valuer = New_df.at[
            index, '9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [Ensim’elec]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + switch_example(valuer)

    if (row['9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [Enigma]']):
        valuer = New_df.at[
            index, '9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [Enigma]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + switch_example(valuer)

    if (row['9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [L\'Ensimien]']):
        valuer = New_df.at[
            index, '9. De quelles associations faites-vous partie ? Ou souhaitez-vous rejoindre? [L\'Ensimien]']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - switch_example(valuer)

    if (row['10. Si on vous donne une imprimante 3D, qu\'est-ce que vous imprimez d’abord ?'] == 'Statue de Mario'):
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1

    if (row[
        '10. Si on vous donne une imprimante 3D, qu\'est-ce que vous imprimez d’abord ?'] == 'Boitier pour sa carte arduino'):
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1

    if (row['10. Si on vous donne une imprimante 3D, qu\'est-ce que vous imprimez d’abord ?'] == 'Des boutons'):
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1

    if (row[
        '10. Si on vous donne une imprimante 3D, qu\'est-ce que vous imprimez d’abord ?'] == 'Une coque de téléphone'):
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1

    if row['11. Quels sont vos hobbies ?']:
        liste_matiere = New_df.at[index, '11. Quels sont vos hobbies ?'].split(",")
        for matiere in liste_matiere:
            if matiere == 'Lecture':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif matiere == 'Bricolage':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            elif matiere == 'Sport':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            elif matiere == 'Art Dessin':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif matiere == 'Jeux vidéos':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif matiere == 'Musique':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
            elif matiere == 'Musculation':
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
            else:
                New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1

    if row['12. Utilisez-vous des sites pour créer une palette de couleurs ?'] == 'oui':
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
    else:
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1

    if (row[
        '13. Votre ordinateur tombe en panne, que faites vous ?'] == 'Vous le démontez pour comprendre d\'où vient le problème'):
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
    if (row[
        '13. Votre ordinateur tombe en panne, que faites vous ?'] == 'Vous essayez de le réparer en passant par le BIOS'):
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + 1
    if row['13. Votre ordinateur tombe en panne, que faites vous ?'] == 'Vous allez voir un réparateur':
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1
    if row['13. Votre ordinateur tombe en panne, que faites vous ?'] == 'Vous en rachetez un':
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] - 1

    if row['14. Qu’avez-vous fait avant le cycle ingénieur ?']:
        valuer = New_df.at[index, '14. Qu’avez-vous fait avant le cycle ingénieur ?']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + switch_example(valuer)

    if row['15. Quel est ton système d’exploitation que tu utilises le plus pour développer ?']:
        valuer = New_df.at[index, '15. Quel est ton système d’exploitation que tu utilises le plus pour développer ?']
        New_df.at[index, 'Notes'] = New_df.at[index, 'Notes'] + switch_example(valuer)
load_df = load(targetfile="transformdata1.csv", data_to_load=New_df)


# New_df['5. Quelle(s) matière(s) avez-vous aimé particulièrement au lycée parmi les suivantes : ']
# New_df


def get_chart_78341403():
    global selected_student
    etudiant = New_df['1. Quel est votre numéro étudiant ? (ex: e22XXXX)']
    n_sup = New_df[(New_df['Notes'] > 0)]['Notes']
    note_sup = n_sup.values
    n_inf = New_df[(New_df['Notes'] < 0)]['Notes']
    note_inf = n_inf.values
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=note_sup,
        y=etudiant,
        marker=dict(color="crimson", size=12),
        mode="markers",
        name="ASTRE",
    ))

    fig.add_trace(go.Scatter(
        x=note_inf,
        y=etudiant,
        marker=dict(color="gold", size=12),
        mode="markers",
        name="IPS",
    ))
    # Check if a student is selected
    if selected_student:
        # Get the data for the selected student
        student_data = New_df[New_df['1. Quel est votre numéro étudiant ? (ex: e22XXXX)'] == selected_student]
        note = student_data['Notes'].values[0]
        # Add a trace for the selected student
        fig.add_trace(go.Scatter(
            x=[note],
            y=[selected_student],
            marker=dict(color="blue", size=20),
            mode="markers",
            name=selected_student,
        ))

    #fig.go.Scatter: data
    fig.update_layout(title="Astre/Ips", xaxis_title="Notes", yaxis_title="Numéro Etudiant")

    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)

# First, create a global variable to store the selected student ID
selected_student = None

# Add a callback function to update the selected student ID when a new value is selected
def update_student(value):
    global selected_student
    selected_student = value
    st.write(f"Selected student: {selected_student}")


if __name__ == '__main__':
    st.title("ASTRE/IPS")
    st.sidebar.header("Listes des étudiants")

    # Sélection des colonnes à afficher
    cols = New_df.columns.tolist()
    selected_cols = st.sidebar.multiselect('Select columns', cols)

    # In the sidebar, add a dropdown menu for selecting a student ID
    student_options = New_df['1. Quel est votre numéro étudiant ? (ex: e22XXXX)'].unique().tolist()
    selected_student = st.sidebar.selectbox("Select a student", student_options, format_func=lambda x: f"{x}", key='select_student')

    #selected_index = selected_cols.index()
    cold = New_df[selected_cols]
    # Affichage des colonnes sélectionnées
    st.sidebar.dataframe(cold)
    get_chart_78341403()
    # Listen for changes on the selectbox
    #st.sidebar.set_event_on_change("select_student", update_student)
