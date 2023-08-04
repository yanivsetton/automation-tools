import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import os
import subprocess

app = FastAPI()

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

def run_script(script_name, db_name, db_host, db_password):
    script_path = os.path.join('./', script_name)
    try:
        result = subprocess.run(['powershell', '-File', script_path, db_name, db_host, db_password], capture_output=True, text=True, check=True)
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.stderr}
    except Exception as e:
        return {"status": "error", "output": str(e)}
    
def run_script_without(script_name):
    script_path = os.path.join('./', script_name)
    try:
        result = subprocess.run(['powershell', '-File', script_path], capture_output=True, text=True, check=True)
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.stderr}
    except Exception as e:
        return {"status": "error", "output": str(e)}

@app.get("/run/{script_name}")
async def execute_script(script_name: str, db_name: str = None, db_host: str = None, db_password: str = None):
    logging.info(f"Received request to run script: {script_name}")
    try:
        result = run_script(script_name, db_name, db_host, db_password)
        if result["status"] == "success":
            logging.info(f"Successfully ran script: {script_name}")
        else:
            logging.error(f"Error running script: {script_name}, Error: {result['output']}")
        return result
    except Exception as e:
        logging.error(f"Error running script: {script_name}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/run_no_params/{script_name}")
async def execute_script_no_params(script_name: str):
    logging.info(f"Received request to run script: {script_name}")
    try:
        result = run_script_without(script_name)
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
    files = os.listdir('./')
    files = [f for f in files if f.endswith('.ps1')]
    html_content = f"""
        <html>
        <head>
         <link rel="icon" type="image/x-icon" href="https://scontent.ftlv23-1.fna.fbcdn.net/v/t39.30808-6/358128517_269808518983651_1245027130833259337_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=6OGDy8kN7PUAX_d1x1t&_nc_ht=scontent.ftlv23-1.fna&oh=00_AfBAUMO0T7NClheE-rEKY3uEkA0V8M9-VCryX4Dn4EbeGQ&oe=64D11DEC"> 
        <title>Set up your Env</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"></script>
        <style>
            #scripts_area {{
                font-family: Arial, sans-serif; /* A clean, modern font */
                color: #333; /* Darker text for better readability */
                padding: 20px; /* Padding around the content for breathing space */
            }}

            #scripts_area table {{
                width: 100%; /* Make the table take up the full width of its parent */
                border-collapse: collapse; /* Collapse table borders into a single border */
            }}

            #scripts_area th, #scripts_area td {{
                border: 1px solid #ddd; /* Light grey border around table cells */
                padding: 15px; /* Padding inside cells for better legibility */
                text-align: left; /* Left-aligned text in cells */
            }}

            #scripts_area th {{
                background-color: #f8f9fa; /* Light grey background for headers */
                color: #333; /* Dark text on light background for headers */
                font-weight: bold; /* Bold text for headers */
            }}

            #scripts_area tr:nth-child(even) {{
                background-color: #f2f2f2; /* Light grey background for every other row */
            }}

            td:hover {{
                background-color: #cff7fc;  /* Change to the color you want */
            }}
            
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
                font-family: Arial, sans-serif; /* Experiment with different fonts */
            }}

            .sidenav button {{
                padding: 12px 16px; /* Increase padding */
                text-decoration: none;
                font-size: 18px; /* Adjust font size */
                color: #ccc; /* Lighten the text color for more contrast */
                display: block;
                border: none;
                background: none;
                transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease; /* Smoothly transition the box-shadow */
                text-align: left;
                width: 100%;
                line-height: 1.6; /* Adjust line height for readability */
            }}

            .sidenav button:hover {{
                color: #fff; /* Lighten the hover text color for more contrast */
                background-color: #333; /* Darken the hover background color for more contrast */
                box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            }}

            .main {{
                margin-left: 190px; /* distance from the sidebar */
                font-size: 20px; /* reduced font size to a more typical size for body text */
                padding: 60px; /* increased padding for more space around the content */
                line-height: 1.6; /* improved line spacing for readability */
                color: #333; /* darker text for better readability */
                font-family: 'Arial', sans-serif; /* cleaner, modern font */
            }}

            .header {{
                display: flex;
                align-items: center;
                justify-content: space-between; /* space out items evenly */
                padding-bottom: 20px; /* add some space below the header */
                border-bottom: 1px solid #ddd; /* a line below the header to separate it from the content */
            }}

            .header img {{
                width: 180px; /* slightly smaller image size for a more balanced look */
                margin-right: 20px;
                border-radius: 5%; /* rounded corners on image for a softer look */
                transition: transform 0.3s ease;
            }}
            
            .header img:hover {{
                transform: scale(1.1);
            }}


            .header h1 {{
                font-size: 32px; /* slightly larger text can look more modern */
                color: #333; /* darker text can often be more readable */
                font-family: 'Arial', sans-serif; /* a cleaner, sans-serif font */
                font-weight: 700; /* make the text bold */
                letter-spacing: -0.5px; /* reducing the space between letters can make the text look more compact and modern */
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1); /* a subtle text shadow can add depth */
                margin: 0; /* remove default margin */
                padding: 0; /* remove default padding */
                line-height: 1.2; /* adjust line height for better readability if your title has more than one line */
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
                padding: 15px;   /* Increased padding for more breathing space */
                font-family: 'Courier New', monospace; /* Switch to a more readable monospace font */
                font-size: 14px; /* Adjust this value as needed */
                line-height: 1.6; /* Adds more space between lines for readability */
                text-shadow: 1px 1px 1px #000; /* Gives a little shadow to the text for better legibility */
            }}

            .log-footer {{
                color: #00FF00;
                font-family: monospace;
            }}

            .modal-dialog {{
                max-width: 500px; /* Increasing the width to allow more space */
                margin: 1.75rem auto; /* Adjusting the margin to center the modal vertically */
            }}

            .modal-content {{
                max-height: 80vh;
                overflow-y: auto;
                border-radius: 15px; /* Adding border-radius to round corners for a more modern look */
                border: none; /* Removing the border for a cleaner look */
                box-shadow: 0 0 30px rgba(0, 0, 0, 0.2); /* Adding a shadow for a more "pop-out" effect */
            }}

            .modal-header {{
                border-bottom: none; /* Removing the line under the header for a cleaner look */
            }}

            .modal-body {{
                font-size: 16px; /* Adjusting font-size for better readability */
            }}

            .modal-footer {{
                border-top: none; /* Removing the line above the footer for a cleaner look */
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
            <button onclick="refreshPage()" style="background: url('https://png.pngtree.com/png-vector/20190420/ourmid/pngtree-reload-vector-icon-png-image_963341.jpg') no-repeat; border: none; width: 50px; height: 50px; background-size: cover; background-position: center;"></button>
        </div>
        <div class="main">
            <div class="header">
                <img src="https://pontera.com/hubfs/Images/Pontera%20Assets/Pontera%20Logos/Stylized-Black-SVG.svg" alt="Pontera Logo">
                <h1>Set up your Env Wizard</h1>
            </div>
            <div id="scripts_area">
            <table class="table table-bordered mt-3">
                <thead>
                    <tr>
                        <th scope="col">Actions:</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Install Dbeaver Community</strong></br></br><p><small><strong>Description:</strong>This will install DBeaver community edition.</small></p><button class="btn btn-primary" onclick="executeScriptNoParams('Install_Dbeaver.ps1')">&#62;</button></td>
                    </tr>
                    <tr>
                        <td colspan="2" style="padding: 0;">
                            <div id="log_Install_Dbeaver.ps1" class="log-container" style="display: none;"></div>
                        </td>
                    </tr>
                     <tr>
                        <td><strong>Install Inteliji Ultimate</strong></br></br><p><small><strong>Description:</strong>This will install Inteliji Ultimate edition.</small></p><button class="btn btn-primary" onclick="executeScriptNoParams('Install_inteliji.ps1')">&#62;</button></td>
                    </tr>
                    <tr>
                        <td colspan="2" style="padding: 0;">
                            <div id="log_Install_inteliji.ps1" class="log-container" style="display: none;"></div>
                    </tr>
                    <tr>
                        <td><strong>Add new DBeaver connection</strong></br></br><p><small><strong>Description:</strong>This will create a new DBeaver profile so you can connect to your Database.</small></p><button class="btn btn-primary" onclick="showScriptParameters('dbeaver-new-connection.ps1')">&#62;</button></td>
                    </tr>
                    <tr>
                        <td colspan="2" style="padding: 0;">
                            <div id="log_dbeaver-new-connection.ps1" class="log-container" style="display: none;"></div>
                        </td>
                    </tr>
                    <tr>
                        <td><strong>Create Github ssh key</strong></br></br><p><small><strong>Description:</strong>This will add ssh key to gitlab automatically.</small></p><button class="btn btn-primary" onclick="executeScriptNoParams('github-ssh.ps1')">&#62;</button></td>
                    </tr>
                    <tr>
                        <td colspan="2" style="padding: 0;">
                            <div id="log_github-ssh.ps1" class="log-container" style="display: none;"></div>
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
                                <select class="form-control" id="db_name" name="db_name">
                                    <option value="">Please select environment</option>
                                    <option value="Production">Production</option>
                                    <option value="Staging">Staging</option>
                                    <option value="Dev">Dev</option>
                                </select>
                                <p><small><strong>Description:</strong> Please select required Env.</small></p>
                            </div>
                            <div class="form-group">
                                <label for="db_host">DB Host</label>
                                <select class="form-control" id="db_host" name="db_host">
                                    <option value="">Please select URL</option>
                                    <option value="https://pontera.production.com:3306">https://pontera.production.com:3306</option>
                                    <option value="https://pontera.staging.com:3306">https://pontera.staging.com:3306</option>
                                    <option value="localhost:3306">localhost:3306</option>
                                </select>
                                <p><small><strong>Description:</strong>Please select the Database URL.</small></p>
                            </div>
                            <div class="form-group">
                                <label for="db_password">DB Password</label>
                                <input type="password" class="form-control" id="db_password" name="db_password">
                                <p><small><strong>Description:</strong> Please type the Database password.</small></p>
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
        
        async function executeScriptNoParams(scriptName) {
            const response = await fetch(`/run_no_params/${scriptName}`);
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
            <span>Coded with ❤️ by:</span>
            <img src="https://cdn.theorg.com/0e4101a6-2d6e-41e7-afdd-a8f34da300c4_thumb.jpg" alt="Creator's Picture" style="width: 50px; border-radius: 50%;">
        </div>
        </body></html>
        """
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
