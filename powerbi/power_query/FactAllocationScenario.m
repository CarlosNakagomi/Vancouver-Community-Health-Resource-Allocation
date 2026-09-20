let
    Source = Csv.Document(File.Contents(pProjectRoot & "\\outputs\\analytical\\community_priority_and_allocation.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Select = Table.SelectColumns(Headers,{"CH_SA_CODE","ResourcePriorityScore","PriorityRank","AllocationWeight","ScenarioBudgetAllocation","ScenarioClinicalFTEAllocation","ScenarioCommunityCareAllocation"}),
    AddScenario = Table.AddColumn(Select,"Scenario",each "Balanced",type text),
    Typed = Table.TransformColumnTypes(AddScenario,{{"CH_SA_CODE",type text},{"ResourcePriorityScore",type number},{"PriorityRank",Int64.Type},{"AllocationWeight",Percentage.Type},{"ScenarioBudgetAllocation",Currency.Type},{"ScenarioClinicalFTEAllocation",type number},{"ScenarioCommunityCareAllocation",Int64.Type}})
in
    Typed

