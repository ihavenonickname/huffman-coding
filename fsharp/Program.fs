open System

module Huffman =
    type private HuffmanNode =
        | Internal of HuffmanNode * HuffmanNode * int
        | Leaf of char * int

    let private count x xs =
        xs
        |> Seq.where (fun y -> y = x)
        |> Seq.length

    let private weight = function
        | Leaf (_, w) -> w
        | Internal (_, _, w) -> w

    let private merge t1 t2 =
        Internal (t1, t2, weight t1 + weight t2)

    let private joinMaps =
        Map.fold (fun acc key value -> Map.add key value acc)

    let private freq text =
        text
        |> Set.ofSeq
        |> Set.map (fun c -> Leaf (c, count c text))
        |> List.ofSeq

    let rec private huffman freqs =
        match List.sortBy weight freqs with
        | left :: right :: rest -> huffman (merge left right :: rest)
        | [head] -> head
        | [] -> failwith "Empty sequence"

    let private codeTable tree =
        let rec codeTable'  acc code tree =
            match tree with
            | Leaf (c, _) -> Map.add c code acc
            | Internal (left, right, _) ->
                let fromLeft = codeTable' acc (code + "0") left
                let fromRight = codeTable' acc (code + "1") right
                joinMaps fromLeft fromRight

        match tree with
        | Leaf (c, _) -> Map.ofList [(c, "0")]
        | _ -> codeTable' Map.empty "" tree

    let encode text =
        let table =
            text
            |> freq
            |> huffman
            |> codeTable

        text
        |> Seq.map (fun c -> Map.find c table)
        |> Seq.fold (+) ""

[<EntryPoint>]
let main argv =
    let binary (n: int) =
        Convert.ToString(n, 2).PadLeft(8, '0')

    match List.ofArray argv with
    | arg :: _ ->
        arg
        |> Seq.map (int >> binary)
        |> Seq.fold (+) ""
        |> printfn "Original:\n%s"

        printfn "Encoded:\n%s" (Huffman.encode arg)
    | [] -> printfn "%s" "Cannot encode empty sequence"

    0
