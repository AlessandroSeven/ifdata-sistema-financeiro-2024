// Set the project folder to the location where you cloned this repository.
let
    ProjectFolder = "C:\CAMINHO\PARA\PASTA\bu",
    CsvPath = ProjectFolder & "\data\processed\ifdata_2024_modelo_powerbi.csv",
    Source = Csv.Document(
        File.Contents(CsvPath),
        [Delimiter=";", Columns=22, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {
        {"Instituicao", type text}, {"CodigoInstituicao", type text},
        {"NomeConglomeradoPrudencial", type text}, {"CodigoConglomeradoFinanceiro", type text},
        {"CodigoConglomeradoPrudencial", type text}, {"TCB", type text},
        {"DescricaoTCB", type text}, {"SegmentoTCB", type text},
        {"TC_Codigo", type text}, {"TipoControle", type text}, {"TI_Codigo", type text},
        {"Cidade", type text}, {"UF", type text}, {"DataBase", type date},
        {"AtivoTotal_R_mil", Int64.Type}, {"CarteiraCreditoClassificada_R_mil", Int64.Type},
        {"PassivoExigivel_R_mil", Int64.Type}, {"Captacoes_R_mil", Int64.Type},
        {"PatrimonioLiquido_R_mil", Int64.Type}, {"LucroLiquido_R_mil", Int64.Type},
        {"NumeroAgencias", Int64.Type}, {"NumeroPostosAtendimento", Int64.Type}
    }, "pt-BR")
in
    Types
