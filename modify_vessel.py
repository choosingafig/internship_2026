from morphman import manipulate_area

def apply_stenosis(input_path, output_path, location, degree_percentage):
    # morphman uses percentage (e.g., 50 for 50% reduction)
    # location should be a list of [x, y, z]
    
    print(f"Applying {degree_percentage}% stenosis at {location}...")
    
    try:
        # The correct internal function is often 'main_area' or 
        # calling the manipulation logic directly:
        manipulate_area.manipulate_area(
            ifile=input_path,
            ofile=output_path,
            method="stenosis",
            percentage=degree_percentage,
            region_of_interest="commandline",
            region_points=location,
            size=4.0 # Length of the stenosis
        )
        print("Stenosis applied successfully.")
    except AttributeError:
        print("Error: Could not find 'manipulate_area'. Ensure morphman is installed correctly.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example: 50% stenosis at your coordinates
apply_stenosis("model.vtp", "stenosis_50.vtp", [-12.2661, 11.9268, -6.9170], 50)