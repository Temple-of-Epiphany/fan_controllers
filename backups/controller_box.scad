/*
 * Temperature Controller Box
 * 
 * Author: Colin Bitterfield
 * Email: colin@bitterfield.com  
 * Date Created: 2025-08-28
 * Date Updated: 2025-08-28
 * Version: 0.1.0
 *
 * Description: Parametric enclosure for temperature controller boards with display window,
 * cable management, and mounting integration for solar charge controller cooling system
 */

// ===== USER CONFIGURATION =====
component = 1; // 1=front_case, 2=back_panel, 3=assembly_with_board

// ===== BOARD DIMENSIONS (measured from ruler image) =====
board_length = 75;      // PCB length (from ruler)
board_width = 35;       // PCB width (from ruler)
board_thickness = 1.6;  // Standard PCB thickness
display_width = 22.7;   // 4-digit 7-segment display width
display_height = 14.1;  // 4-digit 7-segment display height
display_offset_x = 10;  // Display position from left edge (measured)  
display_offset_y = 35 - 7 - 14.1;   // Position from bottom (board_width - distance_from_top - display_height)

// ===== BOX PARAMETERS (2-piece design) =====
wall_thickness = 2;     // Wall thickness
base_thickness = 2;     // Bottom thickness
back_thickness = 2;     // Back panel thickness
clearance = 1;          // Clearance around board
standoff_height = 4;    // Height of PCB standoffs (reduced for compact design)
standoff_dia = 6;       // Standoff diameter
screw_dia = 2.5;        // Mounting screw diameter (M2.5)
case_lip = 1;           // Back panel overlap lip

// Cable management
cable_dia = 4;          // Sensor cable diameter
blue_connector_width = 15;   // Right blue connector width
blue_connector_height = 10;  // Right blue connector height
jst_connector_width = 7;     // JST 2.54mm connector width
jst_connector_height = 8;    // JST 2.54mm connector height
wire_clearance = 10;         // Extra height for wire connections

// Display window
window_margin = 2;      // Extra margin around display

// Calculate internal dimensions (compact 2-piece design)
internal_length = board_length + 2 * clearance;
internal_width = board_width + 2 * clearance;
internal_height = standoff_height + board_thickness + 8; // 8mm clearance above board (compact)

// Calculate external dimensions
external_length = internal_length + 2 * wall_thickness;
external_width = internal_width + 2 * wall_thickness;
external_height = internal_height + base_thickness;

// Back panel dimensions (overlaps case edges)
back_length = external_length + 2 * case_lip;
back_width = external_width + 2 * case_lip;

// ===== MODULES =====

module front_case() {
    difference() {
        // Outer shell (no top - open for back panel)
        cube([external_length, external_width, external_height]);
        
        // Inner cavity (goes all the way through top)
        translate([wall_thickness, wall_thickness, base_thickness])
            cube([internal_length, internal_width, internal_height + 1]);
        
        // Back panel lip recess (around top edge)
        translate([wall_thickness - case_lip, wall_thickness - case_lip, external_height - back_thickness])
            cube([internal_length + 2*case_lip, internal_width + 2*case_lip, back_thickness + 1]);
        
        // Sensor cable hole (front)
        translate([external_length/2, -0.1, base_thickness + standoff_height + board_thickness/2])
            rotate([-90, 0, 0])
                cylinder(d=cable_dia + 0.5, h=wall_thickness + 0.2, $fn=20);
        
        // Blue connector side access (right side)
        translate([external_length - wall_thickness - 0.1, wall_thickness + clearance + board_width - 12, 
                   base_thickness + standoff_height])
            cube([wall_thickness + 0.2, blue_connector_width, blue_connector_height]);
        
        // JST connector access slots (left side - 3 connectors)
        for(i = [0:2]) {
            translate([-0.1, wall_thickness + clearance + 8 + i*10, 
                       base_thickness + standoff_height])
                cube([wall_thickness + 0.2, jst_connector_width, jst_connector_height]);
        }
    }
    
    // PCB standoffs
    translate([wall_thickness + clearance, wall_thickness + clearance, base_thickness]) {
        // Four corner standoffs
        standoff(0, 0);
        standoff(board_length, 0);
        standoff(0, board_width);
        standoff(board_length, board_width);
    }
    
    // Rail mounting bracket (mounts flush against right rail)
    bracket_width = 20;
    bracket_thickness = 3;
    
    // Mounting bracket extends from right side
    translate([external_length, 0, 0])
        difference() {
            cube([bracket_thickness, external_width, external_height]);
            
            // Holes to align with rail mounting holes (25% and 75% of rail height)
            // Assuming 31mm rail height for MPPT 100/30
            rail_height = 31;
            first_hole_pos = rail_height * 0.25;   // 7.75mm
            second_hole_pos = rail_height * 0.75;  // 23.25mm
            
            translate([-0.1, external_width/2, first_hole_pos])
                rotate([0, 90, 0])
                    cylinder(d=4.2, h=bracket_thickness + 0.2, $fn=20);
            translate([-0.1, external_width/2, second_hole_pos])
                rotate([0, 90, 0])
                    cylinder(d=4.2, h=bracket_thickness + 0.2, $fn=20);
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

module back_panel() {
    // Calculate connector positions for access holes
    window_x = wall_thickness + clearance + display_offset_x - window_margin;
    window_y = wall_thickness + clearance + display_offset_y - window_margin;
    window_width = display_width + 2 * window_margin;
    window_height = display_height + 2 * window_margin;
    
    difference() {
        // Main back panel (overlaps case edges)
        cube([back_length, back_width, back_thickness]);
        
        // Display window cutout
        translate([case_lip + window_x, case_lip + window_y, -0.1])
            cube([window_width, window_height, back_thickness + 0.2]);
        
        // Blue connector top access
        translate([case_lip + wall_thickness + clearance + board_length - blue_connector_width - 2, 
                   case_lip + wall_thickness + clearance + board_width - 12, -0.1])
            cube([blue_connector_width + 2, blue_connector_height + 2, back_thickness + 0.2]);
        
        // JST connector top access (4 connectors)
        // Left side JST connectors
        for(i = [0:2]) {
            translate([case_lip + wall_thickness + clearance + 2 - 2, 
                       case_lip + wall_thickness + clearance + 8 + i*10 - 1, -0.1])
                cube([jst_connector_width + 2, jst_connector_height + 2, back_thickness + 0.2]);
        }
        
        // Right edge JST connector 
        translate([case_lip + wall_thickness + clearance + board_length - 8, 
                   case_lip + wall_thickness + clearance + 5 - 1, -0.1])
            cube([jst_connector_width + 2, jst_connector_height + 8, back_thickness + 0.2]);
        
        // Ventilation holes pattern (avoid connector areas)
        vent_spacing = 6;
        vent_dia = 2;
        
        for (x = [vent_spacing : vent_spacing : back_length - vent_spacing]) {
            for (y = [vent_spacing : vent_spacing : back_width - vent_spacing]) {
                // Skip holes in display and connector areas (similar logic with offset for lip)
                display_conflict = (x >= case_lip + window_x - vent_dia && x <= case_lip + window_x + window_width + vent_dia &&
                                   y >= case_lip + window_y - vent_dia && y <= case_lip + window_y + window_height + vent_dia);
                
                if (!display_conflict) {
                    translate([x, y, -0.1])
                        cylinder(d=vent_dia, h=back_thickness + 0.2, $fn=10);
                }
            }
        }
        
        // Corner screw holes for panel attachment
        panel_screw_inset = 3;
        translate([panel_screw_inset, panel_screw_inset, -0.1])
            cylinder(d=2.5, h=back_thickness + 0.2, $fn=20);
        translate([back_length - panel_screw_inset, panel_screw_inset, -0.1])
            cylinder(d=2.5, h=back_thickness + 0.2, $fn=20);
        translate([panel_screw_inset, back_width - panel_screw_inset, -0.1])
            cylinder(d=2.5, h=back_thickness + 0.2, $fn=20);
        translate([back_length - panel_screw_inset, back_width - panel_screw_inset, -0.1])
            cylinder(d=2.5, h=back_thickness + 0.2, $fn=20);
    }
}

module pcb_visualization() {
    // PCB board (75×35mm)
    color("darkgreen") 
        cube([board_length, board_width, board_thickness]);
    
    // 4-digit 7-segment display (22.7×14.1mm, positioned 10mm from left, 7mm from top)
    color("black") 
        translate([display_offset_x, display_offset_y, board_thickness])
            cube([display_width, display_height, 2]);
    
    // 7-segment display digits showing "19.9" (4 digits)
    color("red") 
        translate([display_offset_x + 0.5, display_offset_y + 1, board_thickness + 2.1]) {
            digit_width = (display_width - 1) / 4;  // ~5.4mm per digit
            digit_height = display_height - 2;       // ~12.1mm height
            
            // Digit positions across the display
            for(digit_pos = [0:3]) {
                translate([digit_pos * digit_width, 0, 0]) {
                    // 7-segment pattern (a-g segments)
                    seg_width = digit_width * 0.7;
                    seg_height = digit_height * 0.45;
                    seg_thickness = 0.8;
                    
                    // Horizontal segments (a, d, g)
                    translate([seg_width * 0.1, 0, 0]) 
                        cube([seg_width * 0.8, seg_thickness, 0.1]);  // Top (a)
                    translate([seg_width * 0.1, seg_height, 0]) 
                        cube([seg_width * 0.8, seg_thickness, 0.1]);  // Middle (g)  
                    translate([seg_width * 0.1, seg_height * 2, 0]) 
                        cube([seg_width * 0.8, seg_thickness, 0.1]);  // Bottom (d)
                    
                    // Vertical segments (b, c, e, f)
                    translate([0, seg_thickness, 0]) 
                        cube([seg_thickness, seg_height * 0.8, 0.1]); // Top left (f)
                    translate([seg_width - seg_thickness, seg_thickness, 0]) 
                        cube([seg_thickness, seg_height * 0.8, 0.1]); // Top right (b)
                    translate([0, seg_height + seg_thickness, 0]) 
                        cube([seg_thickness, seg_height * 0.8, 0.1]); // Bottom left (e)
                    translate([seg_width - seg_thickness, seg_height + seg_thickness, 0]) 
                        cube([seg_thickness, seg_height * 0.8, 0.1]); // Bottom right (c)
                }
            }
            
            // Decimal point after third digit (for "19.9")
            translate([3 * digit_width + 0.5, digit_height * 1.8, 0])
                cylinder(d=1, h=0.1, $fn=8);
        }
    
    // Blue connector (top right)
    color("blue") 
        translate([board_length - blue_connector_width - 2, board_width - 12, board_thickness])
            cube([blue_connector_width, blue_connector_height, 6]);
    
    // Red push buttons (3 buttons, first at 16.3mm from left)
    color("red") {
        translate([16.3, 3, board_thickness]) cylinder(d=4, h=1.5, $fn=20);
        translate([26.3, 3, board_thickness]) cylinder(d=4, h=1.5, $fn=20);
        translate([36.3, 3, board_thickness]) cylinder(d=4, h=1.5, $fn=20);
    }
    
    // JST connectors (left side, 3 connectors)
    color("white") {
        for(i = [0:2]) {
            translate([2, 8 + i*10, board_thickness])
                cube([6, jst_connector_width, jst_connector_height]);
        }
    }
    
    // JST connector (right edge)
    color("white") 
        translate([board_length - 8, 5, board_thickness])
            cube([6, jst_connector_width + 8, jst_connector_height]);
    
    // Sensor cable connector
    color("white") {
        translate([board_length/2, 2, board_thickness])
            cube([4, 6, 3]);
        // Cable wire
        translate([board_length/2 + 2, 5, board_thickness + 3])
            cylinder(d=cable_dia, h=15, $fn=20);
    }
    
    // Component chips and capacitors
    color("black") {
        translate([55, 15, board_thickness]) cube([8, 6, 2]);
        translate([45, 25, board_thickness]) cube([6, 4, 1]);
        translate([60, 8, board_thickness]) cube([4, 3, 1.5]);
        // Large capacitor
        translate([10, 20, board_thickness]) cylinder(d=6, h=8, $fn=20);
    }
}

module assembly_with_board() {
    // Front case (transparent)
    color("lightblue", 0.3) front_case();
    
    // PCB in position
    translate([wall_thickness + clearance, wall_thickness + clearance, base_thickness + standoff_height])
        pcb_visualization();
    
    // Back panel (transparent, offset by lip amount)
    color("lightgreen", 0.3) 
        translate([-case_lip, -case_lip, external_height])
            back_panel();
    
    // Show cable routing
    color("red", 0.7) {
        // Sensor cable path
        translate([wall_thickness + clearance + board_length/2, wall_thickness + clearance + 2, 
                   base_thickness + standoff_height + board_thickness + 3])
            cube([2, wall_thickness + clearance - 2, 2]);
    }
}

// ===== MAIN EXECUTION =====
if (component == 1) {
    front_case();
    echo(str("Front case: ", external_length, "×", external_width, "×", external_height, "mm"));
} else if (component == 2) {
    back_panel();
    echo(str("Back panel: ", back_length, "×", back_width, "×", back_thickness, "mm"));
} else if (component == 3) {
    assembly_with_board();
    echo("2-piece assembly view with PCB visualization");
} else {
    echo("ERROR: Component must be 1 (front_case), 2 (back_panel), or 3 (assembly_with_board)");
}

// ===== ASSEMBLY PREVIEW =====
// Uncomment to see assembled view
/*
color("lightblue", 0.7) front_case();
color("lightgreen", 0.7) translate([-case_lip, -case_lip, external_height]) back_panel();
*/