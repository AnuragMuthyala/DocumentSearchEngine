python output_printer.py 0 0 18000000 &
python output_printer.py 1 18000000 35000000 &
python output_printer.py 2 35000000 70000000 &

python search.py $1 $2

python output_handler.py 

rm q_outputs.txt
rm times.txt
rm dummy_output_0.txt
rm dummy_output_1.txt
rm dummy_output_2.txt
rm dummy_ready_0.txt
rm dummy_ready_1.txt
rm dummy_ready_2.txt
rm master_ready.txt