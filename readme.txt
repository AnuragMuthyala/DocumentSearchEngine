For indexing, run the following command:

		bash ./index.sh <path_to_dump> <path_to_dummy>

We are using BSBI approach. The indices are created using three files:

-> dummy_index.py - It processes the files as blocks(1000000 postings) which will be merged later.
-> tf.py - Used for finding number of words in a document for term frequency.
-> result_merge2.py - Used for merging the blocks for creating the final index.

For searching, use the following command

		bash ./search.sh <path_to_index> <query_filename_along_with_path>

-> search.py - processes the query and ranks the document ids accordingly.
-> output_printer.py - prints output in a way understandable by next file.
-> output_handler - prints the required output in queires_op.txt.

Note: For paths, just provide the directory that file is in. Kindly refrain from providing the filename.
