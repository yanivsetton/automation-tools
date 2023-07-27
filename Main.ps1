# Load the Windows Forms assembly
Add-Type -AssemblyName System.Windows.Forms

# Create the form
$form = New-Object Windows.Forms.Form
$form.Text = "RPA - RIP"
$form.Size = New-Object Drawing.Size(800, 650) # Updated size to 250
$form.StartPosition = "CenterScreen"

# Create Labels and TextBoxes for Parameters
$label1 = New-Object Windows.Forms.Label
$label1.Text = "GitHub Token:"
$label1.Location = New-Object Drawing.Point(20, 20)

$textBox1 = New-Object Windows.Forms.TextBox
$textBox1.Location = New-Object Drawing.Point(150, 20)
$textBox1.Size = New-Object Drawing.Size(200, 20)

$label2 = New-Object Windows.Forms.Label
$label2.Text = "Personal Database token:"
$label2.Location = New-Object Drawing.Point(20, 50)

$textBox2 = New-Object Windows.Forms.TextBox
$textBox2.Location = New-Object Drawing.Point(150, 50)
$textBox2.Size = New-Object Drawing.Size(200, 20)

$label3 = New-Object Windows.Forms.Label
$label3.Text = "Password:"
$label3.Location = New-Object Drawing.Point(20, 80)

$textBox3 = New-Object Windows.Forms.TextBox
$textBox3.Location = New-Object Drawing.Point(150, 80)
$textBox3.Size = New-Object Drawing.Size(200, 20)
# Create Progress Bar
$progressBar = New-Object Windows.Forms.ProgressBar
$progressBar.Location = New-Object Drawing.Point(20, 80)
$progressBar.Size = New-Object Drawing.Size(330, 20)

# Progress Bar Label
$progressLabel = New-Object Windows.Forms.Label
$progressLabel.Text = ""
$progressLabel.Location = New-Object Drawing.Point(20, 105)

# Create Execute Button
$executeButton = New-Object Windows.Forms.Button
$executeButton.Text = "Execute"
$executeButton.Location = New-Object Drawing.Point(150, 130)
$executeButton.Add_Click({
    # Get the user input from textboxes
    $param1 = $textBox1.Text
    $param2 = $textBox2.Text

    # Disable the input controls and Execute button
    $textBox1.Enabled = $false
    $textBox2.Enabled = $false
    $testB
    $executeButton.Enabled = $false

    # Script names (replace with your actual scripts' paths)
    $scriptNames = @(
        ".\Install_Dbeaver.ps1",
        ".\Install_inteliji.ps1",
        ".\dbeaver-new-connection.ps1"
    )
    $scriptCount = $scriptNames.Count
    $scriptProgress = 100 / $scriptCount

    for ($scriptIndex = 0; $scriptIndex -lt $scriptCount; $scriptIndex++) {
        $scriptPath = $scriptNames[$scriptIndex]
        $scriptName = [System.IO.Path]::GetFileNameWithoutExtension($scriptPath)

        # Update the progress bar label
        $progressLabel.Text = "Running: $scriptName"
        $form.Refresh()

        # Execute the script using Invoke-Expression (iex)
        Invoke-Expression -Command "& `"$scriptPath`" -param1 `"$param1`" -param2 `"$param2`""

        # Update the progress bar
        $progressBar.Value = ($scriptProgress * ($scriptIndex + 1))
        $form.Refresh() # Refresh the form to show updated progress
    }

    # Show a completion message
    [System.Windows.Forms.MessageBox]::Show("All scripts execution completed!", "Finished", "OK", "Information")

    # Reset the progress bar label
    $progressLabel.Text = ""

    # Re-enable the input controls and Execute button after execution
    $textBox1.Enabled = $true
    $textBox2.Enabled = $true
    $executeButton.Enabled = $true
})

# Add controls to the form
$form.Controls.Add($label1)
$form.Controls.Add($textBox1)
$form.Controls.Add($label2)
$form.Controls.Add($textBox2)
$form.Controls.Add($progressBar)
$form.Controls.Add($progressLabel)
$form.Controls.Add($executeButton)

# Show the form
$form.ShowDialog()
