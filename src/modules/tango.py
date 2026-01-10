from datetime import datetime
class Zip:
    def build_instructions(self, filename):
        # arr, grid_size = analyze_image(filename)
        #
        # chunks = split_into_chunks(arr, grid_size)
        #
        # start_top = find_starting_chunk(chunks, "top")
        # # start_bottom = find_starting_chunk(chunks,"bottom")
        #
        #
        # edge_map = build_edge_map(chunks)
        #
        # path_grid = trace_path(start_top, edge_map)
        # # path_grid = trace_path(start_bottom, edge_map)
        return path_grid

    def download_image(self):
        REFERENCE_DATE = datetime(2026, 1, 9)
        REFERENCE_NUMBER = 298

        today = datetime.now().date()
        today_dt = datetime.combine(today, datetime.min.time())

        days_diff = (today_dt - REFERENCE_DATE).days

        today_number = REFERENCE_NUMBER + days_diff

        base_url = "https://tryhardguides.com/wp-content/uploads/2025/05/Zip-answer-"
        image_url = f"{base_url}{today_number}.jpg"

        filename = f"zip_answer_{today_number}.png"

        print(f"Today's date: {today.strftime('%Y-%m-%d')}")
        print(f"LinkedIn ZIP Puzzle number: #{today_number}")
        print(f"Downloading from: {image_url}\n")


        success = download_helper(image_url, filename)
        
        if not success:
            print("\nTip: Try running again later – TryHardGuides usually uploads early in the day.")
            print("You can also check manually: https://tryhardguides.com/linkedin-zip-answer-today/")
            return None

        return filename

