import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import os
import subprocess

app = FastAPI()

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

def run_script(script_name, db_name, db_host, db_password, personal_secret):
    script_path = os.path.join('./scripts', script_name)
    try:
        result = subprocess.run(['powershell', '-File', script_path, db_name, db_host, db_password, personal_secret], capture_output=True, text=True, check=True)
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.stderr}
    except Exception as e:
        return {"status": "error", "output": str(e)}

@app.get("/run/{script_name}")
async def execute_script(script_name: str, db_name: str = None, db_host: str = None, db_password: str = None, personal_secret: str = None):
    logging.info(f"Received request to run script: {script_name}")
    try:
        result = run_script(script_name, db_name, db_host, db_password, personal_secret)
        if result["status"] == "success":
            logging.info(f"Successfully ran script: {script_name}")
        else:
            logging.error(f"Error running script: {script_name}, Error: {result['output']}")
        return result
    except Exception as e:
        logging.error(f"Error running script: {script_name}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_item():
    logging.info("Received request for the homepage")
    files = os.listdir('./scripts')
    files = [f for f in files if f.endswith('.ps1')]
    html_content = f"""
        <html>
        <head>
        <link rel="icon" type="image/x-icon" href="https://scontent.ftlv23-1.fna.fbcdn.net/v/t39.30808-6/358128517_269808518983651_1245027130833259337_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=6OGDy8kN7PUAX_d1x1t&_nc_ht=scontent.ftlv23-1.fna&oh=00_AfBAUMO0T7NClheE-rEKY3uEkA0V8M9-VCryX4Dn4EbeGQ&oe=64D11DEC">
        <title>Scripts Installation</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"></script>
        <style>
            .sidenav {{
                height: 100%;
                width: 200px;
                position: fixed;
                z-index: 1;
                top: 0;
                left: 0;
                background-color: #111;
                overflow-x: hidden;
                padding-top: 20px;
            }}

            .sidenav button {{
                padding: 6px 8px 6px 16px;
                text-decoration: none;
                font-size: 25px;
                color: #818181;
                display: block;
                border: none;
                background: none;
            }}

            .sidenav button:hover {{
                color: #f1f1f1;
            }}

            .main {{
                margin-left: 200px;
                font-size: 28px;
                padding: 0px 10px;
            }}

            .header {{
                display: flex;
                align-items: center;
            }}

            .header img {{
                width: 200px;
                margin-right: 20px;
            }}

            .header h1 {{
                font-size: 28px;
            }}

            .footer {{
                position: fixed;
                bottom: 0;
                right: 0;
                text-align: right;
                margin-top: 30px;
                color: black;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                z-index: 100;
            }}

            .footer img {{
                width: 50px;
                border-radius: 50%;
                margin-left: 10px;
            }}

            .footer span {{
                margin-right: 10px;
            }}

            .log-container {{
                max-height: 200px;
                overflow-y: auto;
                background-color: #333;
                color: #00FF00;  /* Green color */
                padding: 10px;
                font-family: monospace;
            }}

            .log-footer {{
                color: #00FF00;
                font-family: monospace;
            }}

            .modal-dialog {{
                max-width: 400px;
            }}

            .modal-content {{
                max-height: 80vh;
                overflow-y: auto;
            }}

            /* Additional CSS styles for the parameter modal */
            .modal.fade:not(.show) .modal-dialog {{
                transform: translate(0, -25%);
            }}

            @media screen and (max-height: 450px) {{
                .sidenav {{padding-top: 15px;}}
                .sidenav button {{font-size: 18px;}}
            }}
        </style>
        </head>
        <body>
        <div class="sidenav">
            <button onclick="showScripts()">Scripts</button>
            <button onclick="refreshPage()">Refresh</button>
        </div>
        <div class="main">
            <div class="header">
                <img src="https://pontera.com/hubfs/Images/Pontera%20Assets/Pontera%20Logos/Stylized-Black-SVG.svg" alt="Pontera Logo">
                <h1>Scripts Installation</h1>
            </div>
            <table class="table table-bordered mt-3">
        <thead>
            <tr>
                <th scope="col">Script Name</th>
                <th scope="col">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>script1.ps1</td>
                <td>
                    <button class="btn btn-primary" onclick="showScriptParameters('script1.ps1')">&#62;</button>
                </td>
            </tr>
            <tr>
                <td colspan="2" style="padding: 0;">
                    <div id="log_script1.ps1" class="log-container" style="display: none;"></div>
                </td>
            </tr>
            <tr>
                <td>script2.ps1</td>
                <td>
                    <button class="btn btn-primary" onclick="showScriptParameters('script2.ps1')">&#62;</button>
                </td>
            </tr>
            <tr>
                <td colspan="2" style="padding: 0;">
                    <div id="log_script2.ps1" class="log-container" style="display: none;"></div>
                </td>
            </tr>
            <tr>
                <td>script3.ps1</td>
                <td>
                    <button class="btn btn-primary" onclick="showScriptParameters('script3.ps1')">&#62;</button>
                </td>
            </tr>
                <tr>
                <td colspan="2" style="padding: 0;">
                    <div id="log_script3.ps1" class="log-container" style="display: none;"></div>
                </td>
            </tr>
            <tr>
                <td colspan="2" style="padding: 0;">
                    <div id="log_script3.ps1" class="log-container" style="display: none;"></div>
                </td>
            </tr>
            <tr>
                <td>script4.ps1</td>
                <td>
                    <button class="btn btn-primary" onclick="showScriptParameters('script4.ps1')">&#62;</button>
                </td>
            </tr>
                <tr>
                <td colspan="2" style="padding: 0;">
                    <div id="log_script4.ps1" class="log-container" style="display: none;"></div>
                </td>
            </tr>
            <tr>
        </tbody>
    </table>
            
    """
    html_content += """
                </tbody>
            </table>
            </div>
        </div>
        <div class="modal fade" id="scriptParametersModal" tabindex="-1" role="dialog" aria-labelledby="scriptParametersModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="scriptParametersModalLabel">Script Parameters</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <form id="scriptParametersForm">
                            <div class="form-group">
                                <label for="db_name" title="Parameter Name">DB Name</label><br>
                                <input type="text" class="form-control" id="db_name" name="db_name">
                                <p><small><strong>Description:</strong> Please type the Database name.</small></p>
                            </div>
                            <div class="form-group">
                                <label for="db_host">DB Host</label>
                                <input type="text" class="form-control" id="db_host" name="db_host">
                                <p><small><strong>Description:</strong> Please type the Database URL.</small></p>
                            </div>
                            <div class="form-group">
                                <label for="db_password">DB Password</label>
                                <input type="password" class="form-control" id="db_password" name="db_password">
                                <p><small><strong>Description:</strong> Please type the Database password.</small></p>
                            </div>
                            <div class="form-group">
                                <label for="personal_secret">Personal Secret</label>
                                <input type="password" class="form-control" id="personal_secret" name="personal_secret">
                                <p><small><strong>Description:</strong> Please type the Personal secret you got.</small></p>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="executeScriptWithParameters()">Execute</button>
                    </div>
                </div>
            </div>
        </div>
        <script>
        function createOutputModal(output) {
            // Code for output modal
        }
        
        function refreshPage() {
            location.reload();
        }

        function showScriptParameters(scriptName) {
            $('#scriptParametersModal').modal('show');
            $('#scriptParametersForm').attr('data-script-name', scriptName);
        }

        async function executeScriptWithParameters() {
            const scriptName = $('#scriptParametersForm').attr('data-script-name');
            const formData = $('#scriptParametersForm').serializeArray();
            const params = {};
            formData.forEach(({ name, value }) => (params[name] = value));
            const response = await fetch(`/run/${scriptName}?${$.param(params)}`);
            const data = await response.json();
            const logContainer = document.getElementById('log_' + scriptName);
            logContainer.innerHTML = "<pre style='color: #00FF00'>" + data.output + "</pre>";
            logContainer.style.display = 'block';
            if (data.status === 'success') {
                createOutputModal(data.output);
            } else {
                const logFooter = document.createElement('div');
                logFooter.innerHTML = "<pre class='log-footer'>" + data.output + "</pre>";
                logContainer.appendChild(logFooter);
            }

            // Hide the parameters popup after execution
            $('#scriptParametersModal').modal('hide');
        }

        function showScripts() {
            document.getElementById('scripts_area').style.display = 'block';
        }
        </script>
        <div class="footer">
            <span>Created with ❤️ by:</span>
            <img src="https://cdn.theorg.com/0e4101a6-2d6e-41e7-afdd-a8f34da300c4_thumb.jpg" alt="Creator's Picture" style="width: 50px; border-radius: 50%;">
        </div>
        </body></html>
        """
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

