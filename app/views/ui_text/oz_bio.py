from dash import html
import dash_bootstrap_components as dbc

def oz_bio():
    return html.Div(
    dbc.Container([
        html.H2("About Ozlem Polat", className="mb-4 mt-4"),

        html.P("I'm a data scientist and Ph.D. student in Electrical and Computer Engineering at the University of Florida, with a background in manufacturing systems, data analysis, and applied machine learning."),

        html.P("My interests lie in formal methods, intelligent systems, and interdisciplinary problem-solving. I'm especially drawn to Complexity Theory, Probability Theory, Graph Theory and Game theory — core foundations I want to master and apply to build adaptive, intelligent systems. Combining theoretical insights with practical tools like data visualization, algorithm design, and machine learning, is what I enjoy the most!"),

        html.H4("CyberGators Project", className="mt-4"),
        html.P("As team lead and Scrum master of CyberGators, I contribute to both the system graph modeling and resilience evaluation layers. My responsibilities include building interactive Dash components, implementing attack propagation logic, and formalizing attack trees and resilience metrics. I'm currently leading efforts to integrate Bayesian networks, nearest neighbor search, and graph theory into a unified resilience modeling framework. While cybersecurity is the context for this project, I see it as one of many domains where structured thinking, intelligent automation, and formal reasoning can be applied to solve complex problems."),

        html.H4("Technical Skills", className="mt-4"),
        html.P("I work primarily in Python, C++, R, MATLAB, SQL, and JavaScript, and have strong experience with frameworks like Flask, Dash, Pandas, React, and Node for building data applications and pipelines. On the frontend, I use Plotly, Dash Cytoscape, and custom components to develop interactive visualizations and system editors. I'm proficient in Linux, Git, and cloud platforms, and frequently use Jupyter for prototyping, analysis, and experimentation. My work often involves machine learning libraries such as scikit-learn, XGBoost, and PyTorch, and my current focus is on expanding my knowledge in probabilistic modeling, graph algorithms, and real-time systems."),

        html.H4("Industry Experience", className="mt-4"),
        html.P("Before transitioning into tech, I worked for over a decade in the manufacturing and packaging industry, where I served as Chief Scientific Officer, managing product development and operational analytics."),
        html.P("I currently work as a data analyst at a nonprofit organization, where I develop automated data pipelines, generate insights from complex datasets, and support impact-driven decision making."),

        html.H4("Extracurricular Involvement", className="mt-4"),
        html.P("Beyond tech, I'm deeply committed to sustainability, wildlife protection, and community development. I serve on the Neighborhood Initiative Grant Advisory Committee (NIGAC) in Sarasota County and am a lifetime member of the P.E.O. Sisterhood, an international organization that supports educational opportunities for women."),
        html.P("When I'm not lost in code or data, you might catch me riding a horse (or clipping—very therapeutic!), feeding white-tailed deer (I know, I shouldn't—but if you knew how much they love watermelon!), or attempting to propagate plants (with mixed results; finals week tends to decide their fate). I enjoy cycling, hiking (though not in Florida), kayaking, paddle-boarding, and pretty much anything that involves water or the outdoors."),

        html.H4("Aspirations", className="mt-4"),
        html.P("My long-term goal is to master the fundamental theories like complexity, probability, and systems modeling—and apply them to build intelligent, adaptable systems across domains. Whether in robotics, autonomous vehicles, sustainability, or beyond, I strive to stay grounded in the math and theory while creating tools that drive meaningful impact.")
    ])
)
