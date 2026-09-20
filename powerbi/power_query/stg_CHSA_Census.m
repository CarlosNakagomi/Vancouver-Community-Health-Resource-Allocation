let
    Source = Csv.Document(
        File.Contents(pProjectRoot & "\\data\\raw\\BCHACHSAPO.csv"),
        [Delimiter=",", Columns=124, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TrimmedText = Table.TransformColumns(
        Headers,
        List.Transform(Table.ColumnNames(Headers), each {_, (x) => if x is text then Text.Trim(Text.Clean(x)) else x})
    ),
    Typed = Table.TransformColumnTypes(TrimmedText,{
        {"CH_SA_CODE", type text}, {"CH_SA_NAME", type text}, {"CHSRBRL_CL", type text},
        {"CHSPOP_CEN", Int64.Type}, {"HLT_A_CODE", type text}, {"HLT_A_NAME", type text},
        {"HAUTH_CODE", type text}, {"HAUTH_NAME", type text}, {"LG_FRM_DFQ", type text},
        {"LG_FRM_GNR", type number}, {"GRP_A_TTL", Int64.Type}, {"0_14_A_TTL", Int64.Type},
        {"65PLS_A_TL", Int64.Type}, {"OBJECTID", Int64.Type}
    }, "en-CA"),
    PreserveSourceGNR = Table.DuplicateColumn(Typed, "LG_FRM_GNR", "LG_FRM_GNR_SOURCE_VALUE"),
    CleanGNR = Table.TransformColumns(PreserveSourceGNR, {{"LG_FRM_GNR", each if _ >= 0 and _ <= 100 then _ else null, type nullable number}}),
    AddKeyValidation = Table.AddColumn(CleanGNR, "CHSA_Key_Is_Valid", each [CH_SA_CODE] <> null and Text.Length([CH_SA_CODE]) = 4, type logical)
in
    AddKeyValidation

