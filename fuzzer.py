import subprocess
from random import randint
import os

def run(cmd):
    try:
        subprocess.call(cmd, shell=True, timeout=2)
    except Exception:
        return ;

def flip_byte(in_bytes):
    i = randint(0,len(in_bytes))
    c = chr(randint(0,0xFF))
    return in_bytes[:i] + c.encode('utf-8') + in_bytes[i+1:]

def copy_binary():
    with open("license_2", "rb") as orig_f, open("license_2_fuzz", "wb") as new_f:
        new_f.write(flip_byte(orig_f.read()))

def compare(fn1, fn2):
    with open(fn1) as f1, open(fn2) as f2:
        return f1.read()==f2.read()

def check_output():
    run("./license_2 AAAA-Z10N-42-OK > orig_output")
    run("./license_2_fuzz AAAA-Z10N-42-OK > fuzz_output")
    return compare("orig_output", "fuzz_output")

def check_gdb():
    run("echo disassemble main | gdb license_2 > orig_gdb")
    run("echo disassemble main | gdb license_2_fuzz > fuzz_gdb")
    return compare("orig_gdb", "fuzz_gdb")

def check_radare():
    run('echo -e "aaa\ns sym.main\npdf\nquit" | radare2 license_2 > orig_radare')
    run('echo -e "aaa\ns sym.main\npdf\nquit" | radare2 license_2_fuzz > fuzz_radare')
    return compare("orig_radare", "fuzz_radare")

run("cp license_2 license_2_fuzz")

while True:
    copy_binary()
    if check_output and not check_gdb() and not check_radare():
        print("FOUND POSSIBLE FAIL\n\n\n")
        run("tail fuzz_gdb")
        run("tail fuzz_radare")
        raw_input()
