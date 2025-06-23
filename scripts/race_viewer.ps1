# Create a PowerShell GUI for race viewing
Add-Type -AssemblyName System.Windows.Forms

# Create main form
$form = New-Object System.Windows.Forms.Form
$form.Text = "Horse Racing Analyzer"
$form.Size = New-Object System.Drawing.Size(1000,800)
$form.StartPosition = "CenterScreen"

# Create DataGridView for race data
$dataGridView = New-Object System.Windows.Forms.DataGridView
$dataGridView.Size = New-Object System.Drawing.Size(960,600)
$dataGridView.Location = New-Object System.Drawing.Point(20,20)
$dataGridView.AutoSizeColumnsMode = "Fill"
$dataGridView.ReadOnly = $true
$dataGridView.SelectionMode = "FullRowSelect"

# Add columns to DataGridView
$columns = @("Time", "Course", "Race Name", "Class", "Distance", "Forecast", "Tip")
foreach ($column in $columns) {
    $dataGridView.Columns.Add($column, $column)
}

# Add refresh button
$refreshButton = New-Object System.Windows.Forms.Button
$refreshButton.Text = "Refresh Race Data"
$refreshButton.Size = New-Object System.Drawing.Size(120,30)
$refreshButton.Location = New-Object System.Drawing.Point(20,640)
$refreshButton.Add_Click({
    try {
        $dataGridView.Rows.Clear()
        Write-Host "Fetching race data..."
        $raceData = Get-RaceData
        Write-Host "Got $($raceData.Count) races"
        foreach ($race in $raceData) {
            $dataGridView.Rows.Add(
                $race.off_time,
                $race.course,
                $race.race_name,
                $race.race_class,
                $race.distance_round,
                $race.betting_forecast,
                $race.tip
            )
        }
        $statusLabel.Text = "Last updated: $(Get-Date -Format 'HH:mm:ss')"
    } catch {
        Write-Host "Error: $_" -ForegroundColor Red
        $statusLabel.Text = "Error: $_"
    }
})

# Add status label
$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Size = New-Object System.Drawing.Size(200,30)
$statusLabel.Location = New-Object System.Drawing.Point(160,640)

# Add controls to form
$form.Controls.AddRange(@($dataGridView, $refreshButton, $statusLabel))

# Function to get race data
function Get-RaceData {
    $Username = "Rsl5Zbdu66PWZ49ai5dJIdTJ"
    $Password = "v3xrm53ssfc9uQ7S8bdxUFBz"
    $BaseURL = "https://api.theracingapi.com"

    $Base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $Username,$Password)))
    $Headers = @{ Authorization = ("Basic {0}" -f $Base64AuthInfo) }

    try {
        # Get today's date and format it
        $day = "today"
        Write-Host "Fetching data for: $day"
        
        # Build URI with query parameters
        $uri = "$BaseURL/v1/racecards/free?day=$day&region_codes=gb&region_codes=ire"
        Write-Host "Requesting from: $uri"
        
        $response = Invoke-RestMethod -Uri $uri `
                                     -Headers $Headers `
                                     -Method Get
        Write-Host "Response received"
        return $response.racecards
    } catch {
        Write-Host "Error details: $_" -ForegroundColor Red
        Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Error details: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
        return @()
    }
}

# Show form
Write-Host "Starting form..."
$form.ShowDialog()