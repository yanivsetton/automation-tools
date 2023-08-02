import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import os
import subprocess

app = FastAPI()

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

def run_script(script_name, db_name, db_host, db_password, github_token, personal_secret):
    script_path = os.path.join('./scripts', script_name)
    try:
        result = subprocess.run(['pwsh', '-File', script_path, db_name, db_host, db_password, github_token, personal_secret], capture_output=True, text=True, check=True)
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.stderr}
    except Exception as e:
        return {"status": "error", "output": str(e)}

@app.get("/run/{script_name}")
async def execute_script(script_name: str, db_name: str = None, db_host: str = None, db_password: str = None, github_token: str = None, personal_secret: str = None):
    logging.info(f"Received request to run script: {script_name}")
    try:
        result = run_script(script_name, db_name, db_host, db_password, github_token, personal_secret)
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
        <link rel="icon" type="image/svg+xml" href="data:image/png;base64,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">
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
            <div id="scripts_area">
            <table class="table table-bordered mt-3">
                <thead>
                    <tr>
                        <th scope="col">Script Name</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
    """
    for file in files:
        html_content += f"""
                    <tr>
                        <td>{file}</td>
                        <td>
                            <button class="btn btn-primary" onclick="showScriptParameters('{file}')">&#62;</button>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2" style="padding: 0;">
                            <div id="log_{file}" class="log-container" style="display: none;"></div>
                        </td>
                    </tr>
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
                                <label for="github_token">GitHub Token</label>
                                <input type="password" class="form-control" id="github_token" name="github_token">
                                <p><small><strong>Description:</strong> Please type the Github token.</small></p>
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

