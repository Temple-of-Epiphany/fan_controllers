// Debug hole position calculations for SCC020030200

// Model specifications
model_code = "SCC020030200";
model_name = "BlueSolar MPPT 100/30";
total_width = 187;
controller_length = 122;
heatsink_height = 23;
fan_size = 50;

echo("=== MODEL SPECIFICATIONS ===");
echo(str("Model: ", model_name, " (", model_code, ")"));
echo(str("Total Width: ", total_width, "mm"));
echo(str("Controller Length: ", controller_length, "mm"));
echo(str("Heatsink Height: ", heatsink_height, "mm"));
echo(str("Fan Size: ", fan_size, "mm"));

// Fan plate calculations (from front_fan_mount)
echo("\n=== FAN MOUNTING PLATE CALCULATIONS ===");
plate_width = total_width;                    // 187mm
plate_length = fan_size + 4;                  // 54mm
echo(str("Plate dimensions: ", plate_width, " × ", plate_length, "mm"));

// Hole position calculations
rail_actual_height = (fan_size + 4) - heatsink_height;  // (50+4)-23 = 31mm
first_hole = rail_actual_height * 0.25;                 // 31 * 0.25 = 7.75mm
second_hole = rail_actual_height * 0.75;                // 31 * 0.75 = 23.25mm
edge_offset = 8;                                        // 8mm from edges

echo(str("Rail actual height calculation: (", fan_size, " + 4) - ", heatsink_height, " = ", rail_actual_height, "mm"));
echo(str("First hole position: ", rail_actual_height, " × 0.25 = ", first_hole, "mm from bottom"));
echo(str("Second hole position: ", rail_actual_height, " × 0.75 = ", second_hole, "mm from bottom"));
echo(str("Edge offset: ", edge_offset, "mm from left/right edges"));

// Rear grill calculations (from rear_grill)
echo("\n=== REAR GRILL PLATE CALCULATIONS ===");
grill_plate_width = total_width;              // 187mm
grill_plate_length = fan_size + 4;            // 54mm
echo(str("Plate dimensions: ", grill_plate_width, " × ", grill_plate_length, "mm"));

// Same hole calculations
grill_rail_height = (fan_size + 4) - heatsink_height;   // (50+4)-23 = 31mm
grill_first_hole = grill_rail_height * 0.25;            // 31 * 0.25 = 7.75mm
grill_second_hole = grill_rail_height * 0.75;           // 31 * 0.75 = 23.25mm
grill_edge_offset = 8;                                   // 8mm from edges

echo(str("Rail actual height calculation: (", fan_size, " + 4) - ", heatsink_height, " = ", grill_rail_height, "mm"));
echo(str("First hole position: ", grill_rail_height, " × 0.25 = ", grill_first_hole, "mm from bottom"));
echo(str("Second hole position: ", grill_rail_height, " × 0.75 = ", grill_second_hole, "mm from bottom"));
echo(str("Edge offset: ", grill_edge_offset, "mm from left/right edges"));

// Comparison
echo("\n=== COMPARISON ===");
echo(str("Fan plate holes: ", first_hole, "mm and ", second_hole, "mm from bottom"));
echo(str("Grill plate holes: ", grill_first_hole, "mm and ", grill_second_hole, "mm from bottom"));
echo(str("Difference: ", first_hole - grill_first_hole, "mm and ", second_hole - grill_second_hole, "mm"));

// Visual representation
echo("\n=== VISUAL CHECK ===");
echo("Fan mounting plate holes (Y positions):");
echo(str("  Bottom hole: Y = ", first_hole, "mm"));
echo(str("  Top hole: Y = ", second_hole, "mm"));
echo(str("  Distance between holes: ", second_hole - first_hole, "mm"));

// Rail calculations for comparison
echo("\n=== RAIL CALCULATIONS (for reference) ===");
rail_height = (fan_size + 4) - heatsink_height;  // 31mm
rail_first = rail_height * 0.25;                 // 7.75mm
rail_second = rail_height * 0.75;                // 23.25mm
echo(str("Rail height: ", rail_height, "mm"));
echo(str("Rail holes at: ", rail_first, "mm and ", rail_second, "mm from bottom"));

// The issue you're seeing
echo("\n=== REPORTED MISALIGNMENT ===");
echo("Bottom hole: 0.5mm too low on fan plate");
echo("Top hole: 6-8mm too high on fan plate");
echo("");
echo("This suggests the fan plate might be using different calculations than shown");
echo("or there's a coordinate system offset issue.");