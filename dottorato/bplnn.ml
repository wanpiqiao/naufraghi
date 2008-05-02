(* BackPropagation Layered Neural Network                       *)
(* Copyright (c) 2008 Matteo Bertini                            *)

(* ----------------- Extending Array module ------------------- *)
module Array = struct
  include Array

  let reverse array =
    (**
    Array.reverse [|1;2;3;4|];;
    - : int array = [|4; 3; 2; 1|]
    *)
    let len = length array in
    let rget array n _ = array.(len - n - 1) in
    mapi (rget array) array

  let sum array =
    fold_left (+.) 0.0 array

  let map2 f array1 array2 =
    let len1 = Array.length array1
    and len2 = Array.length array2 in
    if len1 = len2 then
      Array.mapi (fun i array1_i -> (f array1_i array2.(i))) array1
    else
      failwith "incompatible lenghts for map2"

  let dot array1 array2 =
    (**
    let a1 = [|1.0; 2.0; 3.0|];;
    let a2 = [|2.0; 2.0; -1.0|];;
    Array.dot a1 a2;;
    - : float = 3.
    let a3 = [|2.0; 2.0;|];;
    Array.dot a1 a3;;
		Exception: Failure "incompatible lenghts for map2".
    *)
    sum (map2 ( *. ) array1 array2)
 
  let for_all f array =
    List.for_all f (Array.to_list array)

  let init_matrix rows cols afunc =
    (**
    let randfunc _ _ = Random.rand (-2.0) 2.0;;
    Array.init_matrix 2 3 randfunc;;
    *)
    let matrix = make_matrix rows cols 0.0 in
		for i = 0 to rows - 1 do
			for j = 0 to cols - 1 do
				matrix.(i).(j) <- afunc i j 
			done;
		done;
		matrix

  let transposed_matrix amatrix =
    (**
    let counter =
      let c = ref 0.0 in
      let count () = c := !c +. 1.0; !c in
      count;;
    let count _ _ = counter();;
    let matrix = Array.init_matrix 2 3 count;;
    val matrix : float array array = [|[|1.; 2.; 3.|]; [|4.; 5.; 6.|]|]
    Array.transposed_matrix matrix;;
    - : float array array = [|[|1.; 4.|]; [|2.; 5.|]; [|3.; 6.|]|]
    *)
    let rows = length(amatrix)
    and cols = length(amatrix.(0))
    and get_t r c = amatrix.(c).(r) in
    init_matrix cols rows get_t
end

(* ----------------- Extending Random module ------------------- *)
module Random = struct
  include Random

  let rand min max =
    (**
    Random.rand (-2.0) 2.0;;
    *)
    min +. (max -. min) *. (float 1.0) (* Random.float bound = [0, bound) *)
end

(* ------------------------- Loss --------------------------- *)

module Sigmoid = struct
  (**
  Sigmoid.func 0.5;;
  - : float = 0.622459331201854593
  Sigmoid.deriv 0.5;;
  - : float = 0.25.
  *)
  let func x =
    1.0 /. (1.0 +. exp(-.x))
  let deriv x =
    x *. (1.0 -. x)
	let loss output target =
	  (**
	  qloss 2.0 1.0;;
	  - : float = 2.
	  *)
	  (deriv output) *. (target -. output)
end

(* ------------------------- Layer --------------------------- *)

module Layer = struct
  type layer = {
    mutable inputs: float array;
    mutable delta_inputs: float array;
    weights: float array array;
    outputs: float array;
    delta_outputs: float array;
  }

  let layer inputs delta_inputs weights outputs delta_outputs = {
    inputs = inputs;
    delta_inputs = delta_inputs;
    weights = weights;
    outputs = outputs;
    delta_outputs = delta_outputs;
  }

  let make_layer n_in n_out =
    (**
    Layer.make_layer 2 3;;
    *)
    let inputs = Array.make n_in 1.0 in
    let delta_inputs = Array.make n_in 0.0 in
    let outputs = Array.make n_out 1.0 in
    let delta_outputs = Array.make n_out 0.0 in
    let rand _ _ = Random.rand (- 0.5) 0.5 in
    let weights = Array.init_matrix n_out n_in rand in
    layer inputs delta_inputs weights outputs delta_outputs

  let propagate alayer =
    (**
    let alayer = Layer.make_layer 2 3;;
    Layer.propagate alayer;;
    *)
    for k = 0 to Array.length(alayer.outputs) - 1 do
      alayer.outputs.(k) <- (Array.dot alayer.weights.(k) alayer.inputs)
    done;
    alayer

  let propagate_inputs alayer inputs =
    (**
    let alayer = Layer.make_layer 3 3;;
    Layer.propagate_inputs alayer [|2.0; 2.0|];;
    *)
    for j = 0 to Array.length(inputs) - 1 do (* bias is the last in alayer.inputs *)
      alayer.inputs.(j) <- inputs.(j)
    done;
    propagate alayer

  let back_propagate alayer =
    (**
    let alayer = Layer.make_layer 2 3;;
    Layer.back_propagate alayer;;
    *)
    let _weights = Array.transposed_matrix alayer.weights in
    let delta_func j =
      Sigmoid.deriv(alayer.inputs.(j)) *. (Array.dot _weights.(j) alayer.delta_outputs) in
    for j = 0 to Array.length(alayer.inputs) - 1 do
      alayer.delta_inputs.(j) <- delta_func j
    done;
    alayer

  let back_propagate_targets alayer targets =
    (**
    let alayer = Layer.make_layer 2 3;;
    Layer.propagate_inputs alayer [|2.0; 2.0|];;
    Layer.back_propagate_targets alayer [|2.0; 2.0; 2.0|];;
    *)
    for k = 0 to Array.length(targets) - 1 do
      alayer.delta_outputs.(k) <- Sigmoid.loss alayer.outputs.(k) targets.(k)
    done;
    back_propagate alayer

  let update_weights alayer learn =
    (**
    let alayer = Layer.make_layer 2 3;;
    Layer.propagate_inputs alayer [|2.0; 2.0|];;
    Layer.back_propagate_targets alayer [|2.0; 2.0; 2.0|];;
    Layer.update_weights alayer 0.05;;
    *)
    let cumulate_weight k j value =
      alayer.weights.(k).(j) <- alayer.weights.(k).(j) +. value
		and n_in = Array.length(alayer.inputs)
		and n_out = Array.length(alayer.outputs) in
	  for j = 0 to n_in - 1 do
	    for k = 0 to n_out - 1 do
	      cumulate_weight k j (learn *. alayer.delta_outputs.(k) *. alayer.inputs.(j))
	    done;
	  done;
	  alayer

  let sq2error alayer targets =
    (**
    let alayer = Layer.make_layer 2 1;;
    Layer.propagate_inputs alayer [|1.0; 1.0|];;
    Layer.sq2error alayer [|0.0|];;
    *)
    let sum_of_squares array = 
      Array.sum (Array.map (fun x -> x**2.0) array) in
    0.5 *. sum_of_squares (Array.map2 (-.) alayer.outputs targets)

  let connect curr_layer next_layer =
    (**
    let in_layer = Layer.make_layer 2 3;;
    let out_layer = Layer.make_layer 3 1;;
    Layer.connect in_layer out_layer;;
    Layer.propagate_inputs in_layer [|1.0; 1.0|];;
    Layer.propagate out_layer;;
    Layer.back_propagate_targets out_layer [|0.0|];;
    Layer.back_propagate in_layer;;
    *)
    next_layer.inputs <- curr_layer.outputs;
    next_layer.delta_inputs <- curr_layer.delta_outputs;
    [| curr_layer; next_layer |]

end

(* --------------------- ShallowNetwork ----------------------- *)

module ShallowNetwork = struct
  type network = {
    in_layer: Layer.layer;
    out_layer: Layer.layer;
  }
  
  let network in_layer out_layer = {
    in_layer = in_layer;
    out_layer = out_layer;
  }

  let make_network n_in n_hid n_out =
    (**
    let anet = ShallowNetwork.make_network 2 3 1;;
    *)
    let in_layer = Layer.make_layer (n_in + 1) n_hid (* bias *)
    and out_layer = Layer.make_layer n_hid n_out in
    let _ = Layer.connect in_layer out_layer in
    network in_layer out_layer

  let propagate anetwork inputs =
    let _ = Layer.propagate_inputs anetwork.in_layer inputs in
    let _ = Layer.propagate anetwork.out_layer in
    anetwork

  let back_propagate anetwork targets =
    let _ = Layer.back_propagate_targets anetwork.out_layer targets in
    let _ = Layer.back_propagate anetwork.in_layer in
    anetwork

  let update_weights anetwork learn =
    let _ = Layer.update_weights anetwork.in_layer learn in
    let _ = Layer.update_weights anetwork.out_layer learn in
    anetwork

  let sq2error anetwork targets =
    (**
    let anet = ShallowNetwork.make_network 2 3 1;;
    ShallowNetwork.propagate anet [|1.0; 1.0|];;
    ShallowNetwork.back_propagate anet [|0.0|];;
    ShallowNetwork.update_weights anet 0.05;;
    ShallowNetwork.sq2error anet [|0.0|];;
    *)
    Layer.sq2error anetwork.out_layer targets

  let train anetwork inputs targets iterations learn =
    (**
    let anet = ShallowNetwork.make_network 2 5 1;;
    let inputs = [|
                  [|1.0; 1.0|];
                  [|1.0; 0.0|];
                  [|0.0; 1.0|];
                  [|0.0; 0.0|];
                 |];;
    let targets = [|
                   [|0.0|];
                   [|1.0|];
                   [|1.0|];
                   [|0.0|];
                  |];;
    ShallowNetwork.train anet inputs targets 10 0.05;;
    *)
    for count = 0 to iterations do
      let error = ref 0.0 in
			let print = (count mod 1) == 0 in
      if print then
        Printf.printf "iter(%d)\n" count;
      for i = 0 to Array.length(inputs) - 1 do
        let _ = propagate anetwork inputs.(i) in
        let _ = back_propagate anetwork targets.(i) in
        let _ = update_weights anetwork learn in
				let item_error = sq2error anetwork targets.(i) in
        error := !error +. item_error;
	      if print then
	        Printf.printf "  item(%d) item_error: %f\n" i item_error;
      done;
      if print then
        Printf.printf "iter(%d) error: %f\n" count !error;
    done;
    anetwork

end

let _ =
    let anet = ShallowNetwork.make_network 2 5 1
    and inputs = [|
                  [|1.0; 1.0|];
                  [|1.0; 0.0|];
                  [|0.0; 1.0|];
                  [|0.0; 0.0|];
                 |]
    and targets = [|
                   [|0.0|];
                   [|1.0|];
                   [|1.0|];
                   [|0.0|];
                  |] in
    ShallowNetwork.train anet inputs targets 600 0.05
;;

(* vim:cindent sw=2 sts=2 ts=2 et fdm=marker
 *)
