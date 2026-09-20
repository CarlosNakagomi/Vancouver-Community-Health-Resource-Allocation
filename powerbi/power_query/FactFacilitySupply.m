let
    Source = Csv.Document(File.Contents(pProjectRoot & "\\data\\processed\\fact_facility_supply.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{{"CH_SA_CODE",type text},{"FacilityCount",Int64.Type},{"Hospitals",Int64.Type},{"Ambulatory health care services",Int64.Type},{"Nursing and residential care facilities",Int64.Type},{"FacilitiesPer10K",type number},{"PopulationPerFacility",type number},{"HealthcareSupplyScore",type number},{"HealthcareSupplyGapScore",type number}})
in
    Typed

