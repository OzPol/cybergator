from dash import html
import dash_bootstrap_components as dbc

def samson_bio():
    return html.Div([
        dbc.Container([
        html.H2("About Samson Carter", className="mb-4 mt-4"),

        html.P("I'm a software developer and project manager with a background in culinary leadership and operations. After a decade managing " \
        "high-volume food service operations at Disney, Chick-fil-A, and my own catering company, I transitioned into tech with a focus on software" \
        " engineering, cybersecurity, and systems analysis."),

        html.P("I'm passionate about building tools that solve real-world problems, especially in mission-driven environments. I believe " \
        "the best systems are built by diverse, collaborative teams—and I bring that philosophy into every project I work on."),

        html.H4("CyberGators Project", className="mt-4"),
        html.P("As project manager for CyberGators, I coordinated team operations, managed our Jira backlog, drafted the GUI in Figma, and " \
        "worked closely with our backend and frontend developers to align design with implementation. I also contributed to documentation, " \
        "testing, and simulation development, helping guide the project's overall scope and delivery."),

        html.H4("Technical Skills", className="mt-4"),
        html.P("I work primarily in Python, Java, and C++, and I’ve gained experience in Docker, Flask, Dash, and database technologies like" \
        " PostgreSQL and Neo4j. I’m also familiar with frontend technologies and have led cross-functional development teams in both professional"
        " and academic settings."),

        html.H4("Industry Experience", className="mt-4"),
        html.P("Before studying computer science, I worked as a chef, restaurant manager, and business owner. These roles taught me how to lead" \
        " under pressure, solve complex logistical challenges, and communicate effectively across diverse teams. Those skills now support my " \
        "work in tech—particularly in agile environments and stakeholder-facing roles."),

        html.H4("Extracurricular Involvement", className="mt-4"),
        html.P("Outside of class, I enjoy hiking, biking, strength training, playing guitar, and writing poetry. I’m committed to LGBTQ+ " \
        "advocacy, mental health awareness, and lifelong learning."),

        html.H4("Aspirations", className="mt-4"),
        html.P("After graduation, I hope to work as a software engineer or project manager in a field that bridges technology and public " \
        "good—particularly in defense, security, or civic tech. Long-term, I aim to lead teams building software that improves people’s lives "
        "and protects critical systems.")
    ])
    ])