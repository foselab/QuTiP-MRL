from qutip_mrl.synthesis import synth_qc

#circuit synthesis
truth_table = {
    (0,0):0, (0,1):1, (0,2):2, (0,3):3,
    (1,0):0, (1,1):1, (1,2):2, (1,3):3,
    (2,0):0, (2,2):2, (2,3):3,
    (3,0):0, (3,1):1, (3,2):2,
}

qc = synth_qc(
    truth_table,
    base=4,
    num_variables=2,   # a,b
    num_targets=1,     # single output
    output_on="last",
    generations=20000,
    retries=1,
    quiet=False,
)

qc.draw("mpl")
