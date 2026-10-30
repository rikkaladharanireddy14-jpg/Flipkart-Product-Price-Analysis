$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docxPath = (Resolve-Path "final_report\Flipkart_Product_Price_Analysis_Report.docx").Path
$pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")

Write-Host "Opening DOCX: $docxPath"
$doc = $word.Documents.Open($docxPath)

Write-Host "Saving PDF to: $pdfPath"
# 17 represents wdFormatPDF
$doc.SaveAs([ref]$pdfPath, [ref]17)

$doc.Close([ref]$false)
$word.Quit()
Write-Host "Conversion finished successfully!"
