# Copyright 2022 The Explainit Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY aIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import base64
import pathlib

from dash import html

test_png = f"{pathlib.Path(__file__).parent.absolute()}/assets/logo_white.png"
test_base64 = base64.b64encode(open(test_png, "rb").read()).decode("ascii")


def build_banner():
    """
    Creates the main banner for the application.
    """
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Explainit"),
                    html.H6("Understand your data and models like never before."),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="how-it-works", children="How it works?", n_clicks=0
                    ),
                    html.Button(
                        id="learn-more-button", children="STAT-TESTS", n_clicks=0
                    ),
                    html.A(
                        html.Img(
                            id="logo",
                            src=f"data:image/png;base64,{test_base64}",
                        )
                    ),
                ],
            ),
        ],
    )


def generate_section_banner(title):
    """
    Creates a banner for the given title in a dynamic way.

    Args:
        title: value on which to generate the banner.

    Returns:
        HTML division with the generated banner.
    """
    return html.Div(
        className="section-banner",
        children=title,
        style={"font-weight": "bold", "font-size": "15px"},
    )
