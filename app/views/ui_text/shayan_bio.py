from dash import html
import dash_bootstrap_components as dbc

def shayan_bio():
    return html.Div([
    dbc.Container([
        html.H2("About Shayan Akhoondan", className="mb-4 mt-4"),

        html.P("I'm a computer science student with a strong interest in artificial intelligence, machine learning, and system security. My " \
        "work blends algorithmic thinking with hands-on implementation, especially in areas involving modeling, analysis, and simulation."),

        html.H4("CyberGators Project", className="mt-4"),
        html.P("On the CyberGator team, I contributed to full-stack development with a focus on simulation mechanics, user interaction design, "
        "and CVE visualization. I helped prototype new features, implemented UI logic in Dash, and worked on scenarios that test system resilience" \
        " against simulated attacks."),

        html.H4("Research & Technical Skills", className="mt-4"),
        html.P("I have experience working with Python, C++, and TensorFlow, and I’ve built and evaluated convolutional neural networks (CNNs)"
        " for MRI brain scan analysis. I'm comfortable working with algorithms, datasets, and performance metrics, and I enjoy applying technical" \
        " concepts to security challenges."),

        html.H4("Academic Experience", className="mt-4"),
        html.P("Much of my academic work has centered around simulation, resilience, and the intersection of software systems with intelligent " \
        "decision-making. I enjoy solving problems that require both technical depth and creative exploration, particularly in uncertain or adversarial contexts."),

        html.H4("Extracurricular Involvement", className="mt-4"),
        html.P("Outside of school, I enjoy learning about emerging technologies, contributing to small team projects, and exploring topics in " \
        "cryptography, threat modeling, and AI ethics."),

        html.H4("Aspirations", className="mt-4"),
        html.P("After graduation, I hope to pursue graduate study in AI or cybersecurity and work on systems that support national security, " \
        "critical infrastructure, or public safety. I'm excited by projects that require both rigorous research and practical engineering.")
    ])
])
