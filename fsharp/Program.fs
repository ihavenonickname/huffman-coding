open System

module PriorityQueue =
    let private count x xs =
        xs
        |> Seq.where (fun y -> y = x)
        |> Seq.length

    let private normalize queue =
        queue
        |> List.sortBy (fun (_, freq) -> -freq)

    let ofSeq xs =
        xs
        |> Set.ofSeq
        |> Set.map (fun c -> c, count c xs)
        |> Set.toSeq
        |> List.ofSeq
        |> normalize

    let push x weight queue =
        (x, weight) :: queue
        |> normalize

    let pop = function
        | head :: xs -> Some head, xs
        | [] -> None, []

[<EntryPoint>]
let main argv =
    printfn "Hello World from F#!"

    let queue = PriorityQueue.ofSeq "abbccc"

    let rec f queue =
        match PriorityQueue.pop queue with
        | Some x, newQueue ->
            printfn "%O" x
            f newQueue
        | _ -> ()

    f queue |> ignore

    0
