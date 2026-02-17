/*
 * Temperature Controller Box - Reverse Engineered from STL
 * 
 * Author: Colin Bitterfield
 * Email: colin@bitterfield.com  
 * Date Created: 2025-08-28
 * Date Updated: 2025-08-28
 * Version: 0.1.0
 *
 * Description: Reverse engineered from existing STL files:
 * - Front: 77.5×46.4×13.8mm
 * - Back: 76.8×63.6×6.9mm
 */

// ===== USER CONFIGURATION =====
component = 1; // 1=front_case, 2=back_case, 3=assembly

// ===== STL DIMENSIONS (reverse engineered) =====
front_length = 77.5;    // Front case length
front_width = 46.4;     // Front case width  
front_height = 13.8;    // Front case height

back_length = 76.8;     // Back case length
back_width = 63.6;      // Back case width
back_height = 6.9;      // Back case height

// ===== BOARD DIMENSIONS =====
board_length = 75;      // PCB length
board_width = 35;       // PCB width
board_thickness = 1.6;  // PCB thickness

// Display positioning (from your measurements)
display_width = 22.7;
display_height = 14.1;
display_offset_x = 10;
display_offset_y = 35 - 7 - 14.1;  // 7mm from top

// Connector dimensions
blue_connector_width = 15;
blue_connector_height = 10;
jst_connector_width = 7;
jst_connector_height = 8;

// ===== DESIGN PARAMETERS =====
wall_thickness = 2;
clearance = 1;
standoff_height = 4;
standoff_dia = 6;
screw_dia = 2.5;

// ===== MODULES =====

module front_case() {
    difference() {
        // Main body
        cube([front_length, front_width, front_height]);
        
        // Internal cavity
        translate([wall_thickness, wall_thickness, wall_thickness])
            cube([front_length - 2*wall_thickness, 
                  front_width - 2*wall_thickness, 
                  front_height]);
        
        // Display window cutout (positioned based on board layout)
        window_margin = 1;
        window_x = wall_thickness + clearance + display_offset_x - window_margin;
        window_y = wall_thickness + clearance + display_offset_y - window_margin;
        
        translate([window_x, window_y, -0.1])
            cube([display_width + 2*window_margin, 
                  display_height + 2*window_margin, 
                  wall_thickness + 0.2]);
        
        // Blue connector access (top)
        translate([wall_thickness + clearance + board_length - blue_connector_width - 2,
                   wall_thickness + clearance + board_width - 12,
                   -0.1])
            cube([blue_connector_width + 2, blue_connector_height + 2, wall_thickness + 0.2]);
        
        // JST connector access holes (4 connectors)
        // Left side connectors
        for(i = [0:2]) {
            translate([wall_thickness + clearance + 2 - 2,
                       wall_thickness + clearance + 8 + i*10 - 1,
                       -0.1])
                cube([jst_connector_width + 2, jst_connector_height + 2, wall_thickness + 0.2]);
        }
        
        // Right edge connector
        translate([wall_thickness + clearance + board_length - 8,
                   wall_thickness + clearance + 5 - 1,
                   -0.1])
            cube([jst_connector_width + 2, jst_connector_height + 8, wall_thickness + 0.2]);
        
        // Sensor cable hole (front)
        translate([front_length/2, -0.1, front_height/2])
            rotate([-90, 0, 0])
                cylinder(d=4.5, h=wall_thickness + 0.2, $fn=20);
        
        // Side access for blue connector
        translate([front_length - wall_thickness - 0.1, 
                   wall_thickness + clearance + board_width - 12,
                   wall_thickness + standoff_height])
            cube([wall_thickness + 0.2, blue_connector_width, blue_connector_height]);
    }
    
    // PCB standoffs (4 corners)
    translate([wall_thickness + clearance, wall_thickness + clearance, wall_thickness]) {
        standoff(0, 0);
        standoff(board_length, 0);
        standoff(0, board_width);
        standoff(board_length, board_width);
    }
    
    // Mounting tabs for rail integration
    tab_thickness = 3;
    translate([front_length, front_width/2 - tab_thickness/2, 0])
        difference() {
            cube([tab_thickness, tab_thickness, front_height/2]);
            translate([-0.1, tab_thickness/2, front_height/4])
                rotate([0, 90, 0])
                    cylinder(d=4.2, h=tab_thickness + 0.2, $fn=20);
        }
}

module standoff(x, y) {
    translate([x, y, 0]) {
        difference() {
            cylinder(d=standoff_dia, h=standoff_height, $fn=20);
            translate([0, 0, -0.1])
                cylinder(d=screw_dia, h=standoff_height + 0.2, $fn=20);
        }
    }
}

module back_case() {
    difference() {
        // Main back plate
        cube([back_length, back_width, back_height]);
        
        // Ventilation holes pattern
        vent_spacing = 6;
        vent_dia = 2;
        
        for (x = [vent_spacing : vent_spacing : back_length - vent_spacing]) {
            for (y = [vent_spacing : vent_spacing : back_width - vent_spacing]) {
                translate([x, y, -0.1])
                    cylinder(d=vent_dia, h=back_height + 0.2, $fn=10);
            }
        }
        
        // Corner screw holes
        corner_inset = 4;
        translate([corner_inset, corner_inset, -0.1])
            cylinder(d=2.5, h=back_height + 0.2, $fn=20);
        translate([back_length - corner_inset, corner_inset, -0.1])
            cylinder(d=2.5, h=back_height + 0.2, $fn=20);
        translate([corner_inset, back_width - corner_inset, -0.1])
            cylinder(d=2.5, h=back_height + 0.2, $fn=20);
        translate([back_length - corner_inset, back_width - corner_inset, -0.1])
            cylinder(d=2.5, h=back_height + 0.2, $fn=20);
    }
}

module assembly() {
    color("lightblue", 0.7) front_case();
    color("lightgreen", 0.7) translate([0, 0, front_height]) back_case();
}

// ===== MAIN EXECUTION =====
if (component == 1) {
    front_case();
    echo(str("Front case: ", front_length, "×", front_width, "×", front_height, "mm"));
} else if (component == 2) {
    back_case(); 
    echo(str("Back case: ", back_length, "×", back_width, "×", back_height, "mm"));
} else if (component == 3) {
    assembly();
    echo("Assembly view");
} else {
    echo("ERROR: Component must be 1 (front), 2 (back), or 3 (assembly)");
}