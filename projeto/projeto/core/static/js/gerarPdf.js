function gerarPdf(lista, periodo, tipo)
{
	let data = new Date();
	data = data.getDate() + "/" + data.getMonth() + "/" + data.getFullYear()
	let imagem = carregarDados('../scripts/loadImage.php')
	console.log(lista)
	
						let body = [
							[{text: 'Header with Colspan = 2', style: 'tableHeader', colSpan: 2, alignment: 'center'}, {}, {text: 'Header 3', style: 'tableHeader', alignment: 'center'}],
							[{text: 'Header 1', style: 'tableHeader', alignment: 'center'}, {text: 'Header 2', style: 'tableHeader', alignment: 'center'}, {text: 'Header 3', style: 'tableHeader', alignment: 'center'}],
							['Sample value 1', 'Sample value 2', 'Sample value 3'],
							[{rowSpan: 3, text: 'rowSpan set to 3\nLorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor'}, 'Sample value 2', 'Sample value 3'],
							['', 'Sample value 2', 'Sample value 3'],
							['Sample value 1', 'Sample value 2', 'Sample value 3'],
							['Sample value 1', {colSpan: 2, rowSpan: 2, text: 'Both:\nrowSpan and colSpan\ncan be defined at the same time'}, ''],
							['Sample value 1', '', ''],
						]
						console.log(body)
	let doc = 
	{
		content: 
		[
			{image: imagem, width: 300, alignment: 'center'},
			{text: 'Relatório Finaceiro', style: 'header'},
			{text: 'Tipo de Agrupamento: ' + tipo, style: 'header'},
			{text: 'Periodo: ' + periodo, style: 'header'},
			{text: 'Data: ' + data, style: 'header'},
			{
				style: 'table',
				table: {
					widths: [200, '*', '*', '*'],
					body: lista
				}
			}
		],
		styles: 
		{
			meinLogo: {alignment: 'center', width: 100, margin: [10, 10, 10, 10]},
			th: {alignment: 'center', bold: true, fillColor: '#ccc', colSpan: 4},
			firstTd: {bold: true},
			header: {fontSize: 20, alignment: 'center', margin: [0, 10, 10, 10]},
			table: {border: 0}
		}
	}
	
	
	pdfMake.createPdf(doc).open();
	//pdfMake.createPdf(doc).download();
	console.log(8)

}