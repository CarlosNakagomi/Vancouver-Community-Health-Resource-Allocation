let
    Source = Csv.Document(File.Contents(pProjectRoot & "\\data\\processed\\fact_community_profile.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Select = Table.SelectColumns(Headers,{"CH_SA_CODE","CH_SA_NAME","CityOverlapShare"}),
    Rename = Table.RenameColumns(Select,{{"CH_SA_CODE","CHSA Code"},{"CH_SA_NAME","CHSA Name"},{"CityOverlapShare","City Overlap Share"}}),
    Typed = Table.TransformColumnTypes(Rename,{{"CHSA Code",type text},{"CHSA Name",type text},{"City Overlap Share",type number}}),
    Unique = Table.Distinct(Typed,{"CHSA Code"})
in
    Unique

