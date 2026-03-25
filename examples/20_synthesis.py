from qutip_mrl.synthesis import synth_qc

# Circuit synthesis
truth_table = {
    (0,0):0, (0,1):1, (0,2):1,
    (1,0):0, (1,1):1, (1,2):2,
    (2,0):0, (2,1):1,   # (2,2) is don't care (missing)
}

qc, code = synth_qc(
    truth_table,
    base=3,
    num_variables=2,   # a,b
    num_targets=1,     # one output f
    output_on="last",  # put f on the last target wire
    generations=1000,
    retries=1,
    quiet=False,
    gate_list=True,
)

print(code)
qc.draw("mpl")
