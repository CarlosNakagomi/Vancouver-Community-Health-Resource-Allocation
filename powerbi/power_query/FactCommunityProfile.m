let
    Source = Csv.Document(File.Contents(pProjectRoot & "\\data\\processed\\fact_community_profile.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{{"CH_SA_CODE",type text},{"CHSPOP_CEN",Int64.Type},{"GRP_A_TTL",Int64.Type},{"0_14_A_TTL",Int64.Type},{"65PLS_A_TL",Int64.Type},{"LG_FRM_GNR",type number},{"YouthShare",Percentage.Type},{"SeniorShare",Percentage.Type},{"CommunityVulnerabilityProxyScore",type number},{"DataBlindspotScore",type number}})
in
    Typed

