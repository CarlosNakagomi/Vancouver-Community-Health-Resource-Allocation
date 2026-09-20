let
    Source = Csv.Document(
        File.Contents(pProjectRoot & "\\data\\raw\\odhf_bdoes_v1.csv"),
        [Delimiter=",", Columns=17, Encoding=1252, QuoteStyle=QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TrimmedText = Table.TransformColumns(
        Headers,
        List.Transform(Table.ColumnNames(Headers), each {_, (x) => if x is text then Text.Trim(Text.Clean(x)) else x})
    ),
    Typed = Table.TransformColumnTypes(TrimmedText,{
        {"index", Int64.Type}, {"facility_name", type text}, {"source_facility_type", type text},
        {"odhf_facility_type", type text}, {"provider", type text}, {"postal_code", type text},
        {"city", type text}, {"province", type text}, {"CSDname", type text}, {"CSDuid", type text},
        {"Pruid", type text}, {"latitude", type number}, {"longitude", type number}
    }, "en-CA"),
    AddProvinceNormalized = Table.AddColumn(Typed, "province_normalized", each Text.Upper([province]), type text),
    AddCityNormalized = Table.AddColumn(AddProvinceNormalized, "city_normalized", each Text.Lower([city]), type text),
    StrictVancouverCandidates = Table.SelectRows(AddCityNormalized, each [province_normalized] = "BC" and [city_normalized] = "vancouver"),
    AddCoordinateStatus = Table.AddColumn(StrictVancouverCandidates, "CoordinateStatus", each if [latitude] = null or [longitude] = null then "Missing" else if [latitude] < -90 or [latitude] > 90 or [longitude] < -180 or [longitude] > 180 then "Invalid" else "Valid", type text)
in
    AddCoordinateStatus

