from dash import html
import dash_bootstrap_components as dbc

def about_me_bio():
    return html.Div([
        html.H5("About Jess Lourenco", className="mt-3"),

        html.P("I'm a software engineer passionate about building resilient, well-architected systems that solve real-world problems."),
        html.P("I feel most at home working with Java (Spring Boot), Go, and JavaScript (MERN), and I have solid experience with both SQL and NoSQL databases, DevOps practices, and cloud infrastructure."),
        html.P("Before transitioning into engineering, I worked for several years as a Product Manager—an experience that continues to shape how I think about users and impact."),

        html.H5("Projects and Research", className="mt-4"),
        html.P("At CyberGators, I lead the backend efforts, defining the system’s architecture and infrastructure, implementing business logic and algorithms, and modeling the databases."),
        html.P("In parallel (and closely tied to this project), I’ve been conducting independent research on cyber resilience evaluation, with a focus on formalizing problems, designing and proving algorithms, reviewing academic literature, and exploring attack graph-based approaches to system security."),

        html.H5("Extracurricular Involvement", className="mt-4"),
        html.P("At the University of Florida, I’m a full-stack developer for the Solar Gators team, where I’m currently building an observability platform with analytics and interactive visualizations."),
        html.P("The platform processes open telemetry data from our solar cars to help field teams monitor performance and make data-driven improvements during testing and races."),

        html.H5("Industry Experience", className="mt-4"),
        html.P("Outside of school, I work as a Java software engineer at Dock, contributing to services that handle over a billion requests per day."),
        html.P("I also volunteer as a Python backend developer at Lacrei Saúde, a platform dedicated to making healthcare more inclusive, safe, and accessible for LGBTQIA+ people in Brazil."),
        html.P("Additionally, I contribute to open source as a maintainer of BuildCli, a command-line tool that streamlines and automates tasks for Java developers."),

        html.H5("Cybersecurity Perspective", className="mt-4"),
        html.P("While cybersecurity isn’t the main focus of my current roles, the past two semesters of studying it have significantly shaped the way I write code—especially through the lens of defensive programming."),
        html.P("In industries like fintech or any platform handling sensitive data, this mindset is crucial to counter the constant threats of fraud and attacks."),

        html.H5("Looking Ahead", className="mt-4"),
        html.P("After graduation, I’m excited to continue growing as a backend engineer and contributing to projects and open source initiatives that use technology to make a positive impact in the world.")
    ])
