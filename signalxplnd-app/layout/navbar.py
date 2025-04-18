from dash import html
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.NavbarBrand("SignalXplnd", className="text-white"),
                href="#",
                style={"textDecoration": "none"}
            ),
            dbc.Nav(
                dbc.NavItem(dbc.Button("Contact Us", href="mailto:data.xplnd@gmail.com", color="light")),
                className="ms-auto"
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4"
)