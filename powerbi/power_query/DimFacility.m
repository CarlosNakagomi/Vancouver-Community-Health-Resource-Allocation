let
    Source = Csv.Document(File.Contents(pProjectRoot & "\\data\\processed\\dim_facility.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{{"CanonicalFacilityID",type text},{"facility_name",type text},{"odhf_facility_type",type text},{"latitude",type number},{"longitude",type number},{"CMNTY_HLTH_SERV_AREA_CODE",type text}}),
    Unique = Table.Distinct(Typed,{"CanonicalFacilityID"})
in
    Unique

