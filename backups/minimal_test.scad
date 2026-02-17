// Minimal test to isolate the issue

// Direct test data for SCC020030200
test_data = ["SCC020030200", "BlueSolar MPPT 100/30", 187, 122, 23, 157, 3, 50, "A1", "sideways_u"];

// Extract values like the functions do
total_width = test_data[2];   // 187
length = test_data[3];         // 122  
heatsink_height = test_data[4]; // 23
fan_type = test_data[7];       // 50

echo("=== EXTRACTED VALUES ===");
echo(str("Fan type: ", fan_type));
echo(str("Heatsink height: ", heatsink_height));

// Calculate holes
rail_height = (fan_type + 4) - heatsink_height;
first = rail_height * 0.25;
second = rail_height * 0.75;

echo(str("Rail height: ", rail_height));
echo(str("First hole: ", first));
echo(str("Second hole: ", second));

// Simple plate with holes
module test_plate(name) {
    difference() {
        cube([187, 54, 6]);
        translate([8, first, -1]) cylinder(d=4.2, h=8);
        translate([8, second, -1]) cylinder(d=4.2, h=8);
    }
    color("red") translate([93.5, 27, 6])
        linear_extrude(1) text(name, size=10, halign="center");
}

// Test if the issue is with variable scope
module scoped_test() {
    // Local calculation
    local_rail = (50 + 4) - 23;
    local_first = local_rail * 0.25;
    local_second = local_rail * 0.75;
    
    echo(str("Local first: ", local_first));
    echo(str("Local second: ", local_second));
    
    translate([0, 60, 0])
    difference() {
        cube([187, 54, 6]);
        translate([8, local_first, -1]) cylinder(d=4.2, h=8);
        translate([8, local_second, -1]) cylinder(d=4.2, h=8);
    }
}

test_plate("GLOBAL");
scoped_test();

// Draw reference lines
color("green", 0.5) {
    translate([0, 7.75, 10]) cube([200, 0.5, 0.5]);  // Expected
    translate([0, 6.4, 10]) cube([200, 0.5, 0.5]);   // Your measurement
    
    translate([40, 0, 10]) rotate([0, 0, 90]) 
        linear_extrude(0.1) text("7.75mm", size=3);
    translate([40, 60, 10]) rotate([0, 0, 90])
        linear_extrude(0.1) text("7.75mm", size=3);
}