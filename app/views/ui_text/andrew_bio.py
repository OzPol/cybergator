from dash import html
import dash_bootstrap_components as dbc

def andrew_bio():
    return html.Div([
    dbc.Container([
        html.H2("About Andrew Ballard", className="mb-4 mt-4"),

        html.P("I'm a computer science student with a focus on frontend development, user interface design, and machine learning applications. " \
        "My technical background includes experience in Dash, React, C++, and Python, with a passion for making data visually intuitive and engaging."),

        html.H4("CyberGators Project", className="mt-4"),
        html.P("For CyberGator, I served as the frontend lead, helping design and implement the layout and navigation structure in Dash. I worked" \
        " closely with the team to build reusable components, ensure visual clarity, and align the user interface with the application's overall " \
        "goals. I also contributed to the resilience visualization tools and worked on simulation output rendering."),

        html.H4("Technical Skills", className="mt-4"),
        html.P("I'm skilled in HTML/CSS, JavaScript, React, Dash, and Python. I’ve worked with tools like Plotly for interactive charting and am " \
        "comfortable integrating data pipelines with visualization frameworks. I’ve also explored machine learning using TensorFlow and worked on" \
        " projects involving image classification and pattern detection."),

        html.H4("Industry & Academic Experience", className="mt-4"),
        html.P("Beyond class projects, I've developed console-based games, built interfaces for small team apps, and served as a SCRUM master on " \
        "a prior engineering capstone. My academic work has reinforced my ability to lead agile teams, communicate across disciplines, and manage" \
        " multiple software deliverables in parallel. I also worked 7 years as a Shipwright Mechanic for the DOD at KingsBay Naval Base."),

        html.H4("Extracurricular Involvement", className="mt-4"),
        html.P("I enjoy working on passion projects that improve accessibility and user experience in digital tools. Outside of tech, I’m a fan " \
        "of gaming, visual storytelling, and building things that feel rewarding to interact with."),

        html.H4("Aspirations", className="mt-4"),
        html.P("After graduation, I hope to work as a frontend or full-stack engineer in a company that values user-centered design. I enjoy turning" \
        " technical complexity into clean, usable interfaces and hope to continue building systems that people actually enjoy using.")
    ])
])
