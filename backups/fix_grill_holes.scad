// Test fix for grill hole alignment
// The issue: Grill holes are 1.35mm too low (6.4mm instead of 7.75mm)

// Let me check if there's a calculation order issue
fan_type = 50;
heatsink = 23;

echo("=== DEBUGGING GRILL HOLE ISSUE ===");

// What the calculation SHOULD produce:
correct_rail_height = (fan_type + 4) - heatsink;  // 31mm
correct_first = correct_rail_height * 0.25;       // 7.75mm
correct_second = correct_rail_height * 0.75;      // 23.25mm

echo(str("Expected first hole: ", correct_first, "mm"));
echo(str("Expected second hole: ", correct_second, "mm"));

// Your measurement shows 6.4mm, which is 1.35mm too low
measured_first = 6.4;
error = measured_first - correct_first;

echo(str("Measured first hole: ", measured_first, "mm"));
echo(str("Error: ", error, "mm (negative means too low)"));

// Check if there's a pattern:
// If first hole is at 6.4mm instead of 7.75mm
// That's a ratio of 6.4/7.75 = 0.826

ratio = measured_first / correct_first;
echo(str("Ratio: ", ratio));

// If the same ratio applies to the second hole:
predicted_second = correct_second * ratio;  // 23.25 * 0.826 = 19.2mm
echo(str("Predicted second hole based on ratio: ", predicted_second, "mm"));

// But you said the top hole is 6-8mm too HIGH
// If correct is 23.25mm and it's 6-8mm too high, that would be 29.25-31.25mm
// That doesn't match the ratio pattern

echo("\n=== HYPOTHESIS ===");
echo("The holes might be calculated from a different reference point");
echo("Or there might be a variable scope issue in the grill module");

// Let's create a fixed version
module fixed_rear_grill() {
    // Hardcoded for SCC020030200
    plate_width = 187;
    plate_length = 54;
    plate_thickness = 6;
    
    // Force correct calculation
    rail_height_fixed = 31;  // (50+4)-23
    first_hole_fixed = 7.75; // 31*0.25
    second_hole_fixed = 23.25; // 31*0.75
    
    difference() {
        cube([plate_width, plate_length, plate_thickness]);
        
        // Holes at CORRECT positions
        translate([8, first_hole_fixed, -0.5])
            cylinder(d=4.2, h=plate_thickness+1);
        translate([8, second_hole_fixed, -0.5])
            cylinder(d=4.2, h=plate_thickness+1);
            
        translate([plate_width-8, first_hole_fixed, -0.5])
            cylinder(d=4.2, h=plate_thickness+1);
        translate([plate_width-8, second_hole_fixed, -0.5])
            cylinder(d=4.2, h=plate_thickness+1);
    }
    
    // Mark the correct positions
    color("green") {
        translate([20, first_hole_fixed, 6]) sphere(d=2);
        translate([20, second_hole_fixed, 6]) sphere(d=2);
    }
}

fixed_rear_grill();