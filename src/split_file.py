# import os
#
#
# def split_file(input_file, chunk_size, output_dir):
#     try:
#         with open(input_file, 'rb') as f:
#             # Read the entire file into memory
#             content = f.read()
#
#             # Calculate the number of chunks
#             num_chunks = len(content) // chunk_size
#
#             # Create the output directory if it doesn't exist
#
#             # Split the file into chunks
#             for i in range(num_chunks + 1):
#                 start = i * chunk_size
#                 end = min((i + 1) * chunk_size, len(content))
#                 chunk_data = content[start:end]
#                 output_file = os.path.join(output_dir, f'{input_file}.part{i + 1}')
#                 with open(output_file, 'wb') as chunk_file:
#                     chunk_file.write(chunk_data)
#                 print(f'Chunk {i + 1} written to {output_file}')
#
#             print('File splitting completed successfully!')
#     except Exception as e:
#         print(f'Error: {e}')
#
#
#
# input_file = r'Memory'  # Replace 'example.mp4' with your MP4 file path
# chunk_size = 512 * 1024  # Chunk size in bytes, here 512KB
# output_dir = r'C:\Users\ASUS\Desktop\HK232\MMT\BTL\BitTorrent\CN_Asignment1\src\Memory'
# split_file(input_file, chunk_size, output_dir)
