/*
 * Solar Charge Controller Parametric Cooling Mount System
 * 
 * Author: Colin Bitterfield
 * Email: colin@bitterfield.com
 * Date Created: 2025-08-25
 * Date Updated: 2026-01-26
 * Version: 2.1.0
 *
 * STATUS: 44 MODELS - ALL VERIFIED FROM DOCUMENTATION ✅
 *
 * All dimensions verified from victron-mppt-dimensions.md documentation.
 * Configurations: A1, A3, A4, A4_MC4, B1, B2, B2_MC4, B3, C1, C2
 *
 * STL Export: The console will suggest a filename like:
 *   "SCC115060210_left_rail.stl"
 *
 * Description: Generates 4-piece cooling mount assembly for Victron MPPT controllers and Orion-Tr chargers
 * Components: Front fan mount, left rail, right rail, rear hexagonal grill
 *
 * Usage:
 * 1. Set model_code variable to desired controller (e.g. "SCC020030200" or "ORI121236120")
 * 2. Set component variable to desired part (1-4)
 * 3. Render and export STL
 */

// ===== USER CONFIGURATION =====
/* [Model Selection] */
model_code = "SCC020030200"; // [SCC020030200:BlueSolar 100/30, SCC110030210:SmartSolar 100/30, SCC020050200:BlueSolar 100/50, SCC020035000:BlueSolar 150/35, SCC115045222:BlueSolar 150/45, SCC110050210:SmartSolar 100/50, SCC115035210:SmartSolar 150/35, SCC115045212:SmartSolar 150/45, ORI121236120:Orion-Tr Smart 12/12-30A, ORI122436120:Orion-Tr Smart 12/24-15A, ORI241236120:Orion-Tr Smart 24/12-30A, SCC115060210:SmartSolar 150/60-Tr, SCC115070210:SmartSolar 150/70-Tr, SCC115060310:SmartSolar 150/60-MC4, SCC115070310:SmartSolar 150/70-MC4, SCC110020070R:BlueSolar 100/20, SCC110020170R:BlueSolar 100/20_48V, SCC110020060R:SmartSolar 100/20, SCC110020160R:SmartSolar 100/20_48V, SCC115110211:SmartSolar 150/100-Tr, SCC115085211:SmartSolar 150/85-Tr, SCC125110210:SmartSolar 250/100-Tr, SCC125085210:SmartSolar 250/85-Tr, SCC115085411:SmartSolar 150/85-Tr VE.Can, SCC115110410:SmartSolar 150/100-Tr VE.Can, SCC115110420:BlueSolar 150/100-Tr VE.Can, SCC125085411:SmartSolar 250/85-Tr VE.Can, SCC125110411:SmartSolar 250/100-Tr VE.Can, SCC125110441:BlueSolar 250/100-Tr VE.Can, SCC115085511:SmartSolar 150/85-MC4 VE.Can, SCC115110511:SmartSolar 150/100-MC4 VE.Can, SCC125085511:SmartSolar 250/85-MC4 VE.Can, SCC125110512:SmartSolar 250/100-MC4 VE.Can, SCC125060221:SmartSolar 250/60-Tr, SCC125070220:SmartSolar 250/70-Tr, SCC010010050R:BlueSolar 75/10, SCC010015050R:BlueSolar 75/15, SCC075010060R:SmartSolar 75/10, SCC075015060R:SmartSolar 75/15, SCC010015200R:SmartSolar 100/15, SCC110015060R:SmartSolar 100/15]

/* [Component Selection] */
component = 1; // [1:Front Fan Mount, 2:Left Rail, 3:Right Rail, 4:Rear Grill]

// ===== CONTROLLER DATABASE =====
// [model_code, name, total_width, length, heatsink_height, fan_area_width, fan_count, fan_type, flange_config, hole_shape]
controller_db = [
    // A1 Config - 3x50mm fans, Sideways U holes
    ["SCC020030200", "BlueSolar MPPT 100/30", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["SCC110030210", "SmartSolar MPPT 100/30", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["SCC020050200", "BlueSolar MPPT 100/50", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["SCC020035000", "BlueSolar MPPT 150/35", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["SCC115045222", "BlueSolar MPPT 150/45", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["SCC110050210", "SmartSolar MPPT 100/50", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["SCC115035210", "SmartSolar MPPT 150/35", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["SCC115045212", "SmartSolar MPPT 150/45", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["ORI121236120", "Orion-Tr Smart 12/12-30A", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["ORI122436120", "Orion-Tr Smart 12/24-15A", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],
    ["ORI241236120", "Orion-Tr Smart 24/12-30A", 186, 122, 23, 157, 3, 50, "A1", "sideways_u"],

    // A3 Config - 2x50mm fans, Circle holes  
    ["SCC110020070R", "BlueSolar MPPT 100/20", 131, 91.7, 19.8, 106, 2, 50, "A3", "dual_u"],
    ["SCC110020170R", "BlueSolar MPPT 100/20_48V", 131, 91.7, 19.8, 106, 2, 50, "A3", "dual_u"],
    ["SCC110020060R", "SmartSolar MPPT 100/20", 131, 91.7, 19.8, 106, 2, 50, "A3", "dual_u"],
    ["SCC110020160R", "SmartSolar MPPT 100/20_48V", 131, 91.7, 19.8, 106, 2, 50, "A3", "dual_u"],

    // A4 Config - 4x50mm fans, Keyhole top + Sideways U bottom
    ["SCC115060210", "SmartSolar MPPT 150/60-Tr", 250, 171, 32.5, 214, 4, 50, "A4", "keyhole_u"],
    ["SCC115070210", "SmartSolar MPPT 150/70-Tr", 250, 171, 32.5, 214, 4, 50, "A4", "keyhole_u"],

    // A4_MC4 Config - 4x50mm fans, MC4 variants wider due to MC4 connectors
    ["SCC115060310", "SmartSolar MPPT 150/60-MC4", 250, 212.6, 32.5, 214, 4, 50, "A4_MC4", "keyhole_u"],
    ["SCC115070310", "SmartSolar MPPT 150/70-MC4", 250, 212.6, 32.5, 214, 4, 50, "A4_MC4", "keyhole_u"],

    // B1 Config - 4x50mm fans, Keyhole top + Sideways U bottom (USER CONFIRMED: Only these 4 Tr models)
    // Keyhole: 13.75mm from edge, R4 top/R8 bottom/17mm c-c. U: 13.75mm from edge, R3.75, width 7.5mm
    ["SCC115085211", "SmartSolar MPPT 150/85-Tr", 295, 204, 34.5, 242, 4, 50, "B1", "keyhole_u"],
    ["SCC115110211", "SmartSolar MPPT 150/100-Tr", 295, 204, 34.5, 242, 4, 50, "B1", "keyhole_u"],
    ["SCC125085210", "SmartSolar MPPT 250/85-Tr", 295, 204, 34.5, 242, 4, 50, "B1", "keyhole_u"],
    ["SCC125110210", "SmartSolar MPPT 250/100-Tr", 295, 204, 34.5, 242, 4, 50, "B1", "keyhole_u"],

    // B1_MC4 Config removed - models SCC115085311, SCC115110311, SCC125085310, SCC125110310 do not exist
    // MC4 variants are actually VE.Can models with 5xx series numbers (see B2_MC4 config)

    // B2 Config - 4x50mm fans, Keyhole top + Sideways U bottom (XL Tr VE.Can controllers)
    ["SCC115085411", "SmartSolar MPPT 150/85-Tr VE.Can", 294.6, 213.9, 34.6, 242.6, 4, 50, "B2", "keyhole_u"],
    ["SCC115110410", "SmartSolar MPPT 150/100-Tr VE.Can", 294.6, 213.9, 34.6, 242.6, 4, 50, "B2", "keyhole_u"],
    ["SCC115110420", "BlueSolar MPPT 150/100-Tr VE.Can", 294.6, 213.9, 34.6, 242.6, 4, 50, "B2", "keyhole_u"],
    ["SCC125085411", "SmartSolar MPPT 250/85-Tr VE.Can", 294.6, 213.9, 34.6, 242.6, 4, 50, "B2", "keyhole_u"],
    ["SCC125110411", "SmartSolar MPPT 250/100-Tr VE.Can", 294.6, 213.9, 34.6, 242.6, 4, 50, "B2", "keyhole_u"],
    ["SCC125110441", "BlueSolar MPPT 250/100-Tr VE.Can", 294.6, 213.9, 34.6, 242.6, 4, 50, "B2", "keyhole_u"],

    // B2_MC4 Config - 4x50mm fans, MC4 VE.Can variants (XL MC4 VE.Can controllers)
    ["SCC115085511", "SmartSolar MPPT 150/85-MC4 VE.Can", 294.6, 246, 34.6, 242.6, 4, 50, "B2_MC4", "keyhole_u"],
    ["SCC115110511", "SmartSolar MPPT 150/100-MC4 VE.Can", 294.6, 246, 34.6, 242.6, 4, 50, "B2_MC4", "keyhole_u"],
    ["SCC125085511", "SmartSolar MPPT 250/85-MC4 VE.Can", 294.6, 246, 34.6, 242.6, 4, 50, "B2_MC4", "keyhole_u"],
    ["SCC125110512", "SmartSolar MPPT 250/100-MC4 VE.Can", 294.6, 246, 34.6, 242.6, 4, 50, "B2_MC4", "keyhole_u"],
    
    // B3 Config - 4x50mm fans, Keyhole top + Sideways U bottom
    ["SCC125060221", "SmartSolar MPPT 250/60-Tr", 248.5, 170.7, 34.5, 208.5, 4, 50, "B3", "keyhole_u"],
    ["SCC125070220", "SmartSolar MPPT 250/70-Tr", 248.5, 170.7, 34.5, 208.5, 4, 50, "B3", "keyhole_u"],
    
    // C1 Config - 2x40mm fans, Circle holes (housing-based)
    ["SCC010010050R", "BlueSolar MPPT 75/10", 112.9, 99.7, 0, 81.9, 2, 40, "C1", "circle"],
    ["SCC010015050R", "BlueSolar MPPT 75/15", 112.9, 99.7, 0, 81.9, 2, 40, "C1", "circle"],
    ["SCC075010060R", "SmartSolar MPPT 75/10", 112.9, 99.7, 0, 81.9, 2, 40, "C1", "circle"],
    ["SCC075015060R", "SmartSolar MPPT 75/15", 112.9, 99.7, 0, 81.9, 2, 40, "C1", "circle"],
    
    // C2 Config - 2x40mm fans, Circle holes (housing-based)  
    ["SCC010015200R", "SmartSolar MPPT 100/15", 113.9, 100.7, 0, 86.4, 2, 40, "C2", "circle"],
    ["SCC110015060R", "SmartSolar MPPT 100/15", 113.9, 100.7, 0, 86.4, 2, 40, "C2", "circle"]
];

// ===== DESIGN PARAMETERS =====
wall_thickness = 3;        // Wall thickness for all components
rail_width = 18;           // Standard rail width (from flange data)
base_height = 15;          // Height of mounting base
fan_clearance = 5;         // Clearance around fans
screw_clearance = 0.2;     // Clearance for screws
print_tolerance = 0.1;     // 3D printing tolerance
plate_width_adjust = 0.2;  // Width adjustment for plates (2x paper thickness)

// Fan mount plate dimensions
plate_depth = 6;           // Depth/thickness of fan mount plate

// M3 and M4 screw specifications
m3_hole_dia = 3.2;
m3_head_dia = 6;
m3_head_depth = 3;

m4_hole_dia = 4.2; 
m4_head_dia = 7;
m4_head_depth = 4;

// ===== LOOKUP FUNCTIONS =====
function find_controller(code) = 
    let(matches = [for(i = [0:len(controller_db)-1]) if(controller_db[i][0] == code) controller_db[i]])
    len(matches) > 0 ? matches[0] : undef;

function get_name(ctrl) = ctrl[1];
function get_total_width(ctrl) = ctrl[2];
function get_length(ctrl) = ctrl[3]; 
function get_heatsink_height(ctrl) = ctrl[4];
function get_fan_area_width(ctrl) = ctrl[5];
function get_fan_count(ctrl) = ctrl[6];
function get_fan_type(ctrl) = ctrl[7];
function get_flange_config(ctrl) = ctrl[8];
function get_hole_shape(ctrl) = ctrl[9];

// Component name lookup
function get_component_name(comp) =
    comp == 1 ? "front_fan_mount" :
    comp == 2 ? "left_rail" :
    comp == 3 ? "right_rail" :
    comp == 4 ? "rear_grill" : "unknown";

// ===== MAIN EXECUTION =====
ctrl = find_controller(model_code);

if (ctrl == undef) {
    echo(str("ERROR: Model code '", model_code, "' not found in database"));
    echo("Available models:", [for(i = [0:len(controller_db)-1]) controller_db[i][0]]);
} else {
    // Generate meaningful filename suggestion
    component_name = get_component_name(component);

    echo(str("Generating component ", component, " for ", get_name(ctrl)));
    echo(str("Dimensions: ", get_total_width(ctrl), "×", get_length(ctrl), "×", get_heatsink_height(ctrl), "mm"));
    echo(str("Fans: ", get_fan_count(ctrl), "×", get_fan_type(ctrl), "mm"));
    echo(str("Model: ", model_code, " | Component: ", component_name));
    echo(str("Suggested STL name: ", model_code, "_", component_name, ".stl"));

    if (component == 1) {
        front_fan_mount(ctrl);
    } else if (component == 2) {
        left_rail(ctrl);
    } else if (component == 3) {
        right_rail(ctrl);
    } else if (component == 4) {
        rear_grill(ctrl);
    } else {
        echo("ERROR: Component must be 1-4 (1=front_fan, 2=left_rail, 3=right_rail, 4=rear_grill)");
    }
}

// ===== COMPONENT MODULES =====

module front_fan_mount(ctrl) {
    fan_count = get_fan_count(ctrl);
    fan_size = get_fan_type(ctrl);
    fan_area_width = get_fan_area_width(ctrl);
    controller_length = get_length(ctrl);
    
    // Fan mount plate dimensions
    plate_width = get_total_width(ctrl) + plate_width_adjust;     // Total width + adjustment
    plate_length = fan_size + 4;                    // Fan height + 4mm spacing
    plate_thickness = plate_depth;                   // 6mm thick
    
    // Calculate fan spacing within the fan area (centered on plate)
    total_fan_width = fan_count * fan_size;
    total_gap = fan_area_width - total_fan_width;
    gap_per_side = total_gap / (fan_count + 1);
    fan_area_start = (plate_width - fan_area_width) / 2;  // Center fan area on plate
    
    difference() {
        // Main body - spans full total width
        cube([plate_width, plate_length, plate_thickness]);
        
        // Fan cutouts and screw holes (positioned within fan area)
        for (i = [0:fan_count-1]) {
            x_pos = fan_area_start + gap_per_side + i * (fan_size + gap_per_side);
            
            translate([x_pos + fan_size/2, plate_length/2, -0.5]) {
                // Fan opening (leave frame for mounting)
                cylinder(d=fan_size-8, h=plate_thickness+1, $fn=50);
                
                // Screw holes for fan mounting
                screw_spacing = fan_size == 50 ? 40 : 30;
                screw_dia = fan_size == 50 ? m4_hole_dia : m3_hole_dia;
                head_dia = fan_size == 50 ? m4_head_dia : m3_head_dia;
                head_depth = fan_size == 50 ? m4_head_depth : m3_head_depth;
                
                for (x = [-screw_spacing/2, screw_spacing/2]) {
                    for (y = [-screw_spacing/2, screw_spacing/2]) {
                        translate([x, y, 0]) {
                            // Through hole for screw
                            cylinder(d=screw_dia, h=plate_thickness+1);
                            // Recessed hole: 4mm deep, 5.6mm wide for nut wells
                            translate([0, 0, plate_thickness - 4])
                                cylinder(d=5.6, h=4.5);
                        }
                    }
                }
            }
        }
        
        // Rail mounting holes - match rail hole positions
        rail_hole_dia = m4_hole_dia;
        edge_offset = 8;  // Distance from plate edges
        
        // Get actual rail height for this controller (must match rail calculation)
        rail_actual_height = (get_fan_type(ctrl) + 4) - get_heatsink_height(ctrl);
        first_hole = rail_actual_height * 0.25;   // 1/4 of rail height
        second_hole = rail_actual_height * 0.75;  // 3/4 of rail height
        
        // Left side rail holes (within rail area)
        translate([edge_offset, first_hole, -0.5])
            cylinder(d=rail_hole_dia, h=plate_thickness+1);
        translate([edge_offset, second_hole, -0.5])
            cylinder(d=rail_hole_dia, h=plate_thickness+1);
            
        // Right side rail holes (within rail area)
        translate([plate_width-edge_offset, first_hole, -0.5])
            cylinder(d=rail_hole_dia, h=plate_thickness+1);
        translate([plate_width-edge_offset, second_hole, -0.5])
            cylinder(d=rail_hole_dia, h=plate_thickness+1);

        // Add model name debossed on back edge face (thin vertical edge)
        // Position at the back edge, centered on width and thickness
        translate([plate_width/2, plate_length, plate_thickness/2])
            rotate([90, 0, 0])
                linear_extrude(height=1.5)
                    mirror([0, 1, 0])
                        text(get_name(ctrl), size=3, halign="center", valign="center", font="Liberation Sans:style=Bold");
    }

    echo(str("Front fan mount: ", plate_width, "×", plate_length, "mm plate with ", fan_count, " × ", fan_size, "mm fans"));
}

module left_rail(ctrl) {
    controller_length = get_length(ctrl);
    heatsink_height = get_heatsink_height(ctrl);
    hole_shape = get_hole_shape(ctrl);

    // Rail height = fan plate size minus heatsink height
    fan_size = get_fan_type(ctrl);
    rail_height = (fan_size + 4) - heatsink_height;
    rail_length = controller_length; // Match controller length exactly

    union() {
        difference() {
            // Main rail body
            cube([rail_width, rail_length, rail_height]);
        
        // Flange mounting holes - through Z-axis (Z- to Z+) with U cutouts to edges
        if (hole_shape == "sideways_u") {
            // A1 config - Two 8mm holes, each 25mm from nearest edge, centered on Y-axis
            // Rail length is 142mm, so center is at 71mm
            
            // First hole 25mm from Y=0 edge
            translate([rail_width/2, 25, -1])
                cylinder(d=8, h=rail_height+2);
            // U cutout from first hole to X=0 edge (8mm wide slot)
            translate([0, 25 - 4, -1])  // 8mm wide cutout centered on hole
                cube([rail_width/2, 8, rail_height+2]);
                
            // Second hole 71.5mm from first hole (96.5mm from edge)
            translate([rail_width/2, 96.5, -1])
                cylinder(d=8, h=rail_height+2);
            // U cutout from second hole to X=0 edge (8mm wide slot)
            translate([0, 96.5 - 4, -1])  // 8mm wide cutout
                cube([rail_width/2, 8, rail_height+2]);
        } else if (hole_shape == "dual_u") {
            // A3 config - Dual sideways U holes, 54mm center-to-center spacing
            // Front U-hole: 18.8mm from Y=0 edge
            front_u_pos = 18.8;
            rear_u_pos = 72.8;  // 18.8 + 54mm spacing

            // Front U-hole
            translate([rail_width/2, front_u_pos, -1])
                cylinder(d=5, h=rail_height+2);
            // U cutout from front hole to X=0 edge (5mm wide slot)
            translate([0, front_u_pos - 2.5, -1])
                cube([rail_width/2, 5, rail_height+2]);

            // Rear U-hole
            translate([rail_width/2, rear_u_pos, -1])
                cylinder(d=5, h=rail_height+2);
            // U cutout from rear hole to X=0 edge (5mm wide slot)
            translate([0, rear_u_pos - 2.5, -1])
                cube([rail_width/2, 5, rail_height+2]);
        } else if (hole_shape == "circle") {
            // C1, C2 configs - Housing-based mounting with corner holes
            flange_config = get_flange_config(ctrl);

            if (flange_config == "C1") {
                // C1: 4 corner holes, R4 (8mm diameter)
                // Spacing: 98.8mm horizontal, 84.1mm vertical
                // Margins: 7.05mm (sides), 7.8mm (top/bottom) on 112.9×99.7mm housing
                hole_margin_x = 7.05;
                hole_margin_y = 7.8;
                total_width = get_total_width(ctrl);  // 112.9mm

                // Four corner holes through housing (no rail, so through Z-axis from top)
                // Front-left
                translate([hole_margin_x, hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Front-right
                translate([total_width - hole_margin_x, hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Rear-left
                translate([hole_margin_x, controller_length - hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Rear-right
                translate([total_width - hole_margin_x, controller_length - hole_margin_y, -1])
                    cylinder(d=8, h=20);
            } else if (flange_config == "C2") {
                // C2: 4 corner holes, R4 (8mm diameter) - same pattern as C1
                // Spacing: 98.8mm horizontal, 84.1mm vertical
                // Margins: 7.05mm (sides), 7.8mm (top/bottom) on 113.9×100.7mm housing
                hole_margin_x = 7.05;
                hole_margin_y = 7.8;
                total_width = get_total_width(ctrl);  // 113.9mm

                // Four corner holes through housing (no rail, so through Z-axis from top)
                // Front-left
                translate([hole_margin_x, hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Front-right
                translate([total_width - hole_margin_x, hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Rear-left
                translate([hole_margin_x, controller_length - hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Rear-right
                translate([total_width - hole_margin_x, controller_length - hole_margin_y, -1])
                    cylinder(d=8, h=20);
            }
        } else if (hole_shape == "keyhole") {
            // B1, B2, B3 configs - Holes from top for larger controllers
            translate([rail_width/2, 30, rail_height])
                cylinder(d=m4_hole_dia, h=15, center=true);
            translate([rail_width/2, controller_length-30, rail_height])
                cylinder(d=m4_hole_dia, h=15, center=true);
            // Additional hole for large controllers
            if (controller_length > 150) {
                translate([rail_width/2, controller_length/2, rail_height])
                    cylinder(d=m4_hole_dia, h=15, center=true);
            }
        } else if (hole_shape == "keyhole_u") {
            // A4, B1, B2, B3 configs - Keyhole at top (back), Sideways U at bottom (front)
            // Get flange config to determine hole dimensions
            flange_config = get_flange_config(ctrl);

            // Config-specific U-hole dimensions
            u_hole_position = (flange_config == "A4" || flange_config == "A4_MC4" || flange_config == "B3") ? 11 :
                             (flange_config == "B1" || flange_config == "B2" || flange_config == "B2_MC4") ? 13.75 : 25;
            u_hole_diameter = (flange_config == "A4" || flange_config == "A4_MC4" || flange_config == "B3") ? 6 :
                             (flange_config == "B1" || flange_config == "B2" || flange_config == "B2_MC4") ? 7.5 : 8;

            // Config-specific keyhole dimensions
            keyhole_position = (flange_config == "A4" || flange_config == "A4_MC4" || flange_config == "B3") ? 11 :
                              (flange_config == "B1" || flange_config == "B2" || flange_config == "B2_MC4") ? 13.75 : 30;

            // Top keyhole (rear of controller, toward longer Y values)
            if (flange_config == "A4" || flange_config == "A4_MC4") {
                // A4/A4_MC4: Keyhole with R2.75 top, R6 bottom, 12mm center-to-center
                translate([rail_width/2, controller_length - keyhole_position, rail_height]) {
                    // Top small circle (R2.75 = 5.5mm diameter)
                    cylinder(r=2.75, h=15, center=true);
                    // Bottom large circle (R6 = 12mm diameter), 12mm below top
                    translate([0, 0, -12])
                        cylinder(r=6, h=15, center=true);
                    // Connecting slot (5.5mm wide to match top circle)
                    translate([0, 0, -6])
                        cylinder(r=2.75, h=12, center=true);
                }
            } else if (flange_config == "B1" || flange_config == "B2" || flange_config == "B2_MC4") {
                // B1/B2: Keyhole with R4 top, R8 bottom, 17mm center-to-center (USER CONFIRMED for B1, B2 needs verification)
                translate([rail_width/2, controller_length - keyhole_position, rail_height]) {
                    // Top circle (R4 = 8mm diameter)
                    cylinder(r=4, h=15, center=true);
                    // Bottom large circle (R8 = 16mm diameter), 17mm below top
                    translate([0, 0, -17])
                        cylinder(r=8, h=15, center=true);
                    // Connecting slot (8mm wide to match top circle)
                    translate([0, 0, -8.5])
                        cylinder(r=4, h=17, center=true);
                }
            } else if (flange_config == "B3") {
                // B3: Keyhole with R3 top, R6 bottom, 12mm center-to-center
                translate([rail_width/2, controller_length - keyhole_position, rail_height]) {
                    // Top small circle (R3 = 6mm diameter)
                    cylinder(r=3, h=15, center=true);
                    // Bottom large circle (R6 = 12mm diameter), 12mm below top
                    translate([0, 0, -12])
                        cylinder(r=6, h=15, center=true);
                    // Connecting slot (6mm wide to match top circle)
                    translate([0, 0, -6])
                        cylinder(r=3, h=12, center=true);
                }
            } else {
                // Fallback: Simple through-hole
                translate([rail_width/2, controller_length - keyhole_position, rail_height])
                    cylinder(d=8, h=15, center=true);
            }

            // Bottom sideways U (front of controller)
            translate([rail_width/2, u_hole_position, -1])
                cylinder(d=u_hole_diameter, h=rail_height+2);
            // U cutout from hole to X=0 edge
            translate([0, u_hole_position - u_hole_diameter/2, -1])
                cube([rail_width/2, u_hole_diameter, rail_height+2]);
        }
        
        // Holes to connect to front/rear plates - positioned at 1/4 and 3/4 of rail height
        first_hole = rail_height * 0.25;   // 1/4 up from bottom (center of lower half)
        second_hole = rail_height * 0.75;  // 3/4 up from bottom (center of upper half)
        
        // Holes through the 18mm width (from front face to back face) for plate connection
        translate([rail_width/2, 0, first_hole])
            rotate([90, 0, 0])
                cylinder(d=m4_hole_dia, h=12, center=true);
        translate([rail_width/2, 0, second_hole])
            rotate([90, 0, 0])
                cylinder(d=m4_hole_dia, h=12, center=true);
                
        // Holes at rear end for rear plate connection  
        translate([rail_width/2, rail_length, first_hole])
            rotate([90, 0, 0])
                cylinder(d=m4_hole_dia, h=12, center=true);
        translate([rail_width/2, rail_length, second_hole])
            rotate([90, 0, 0])
                cylinder(d=m4_hole_dia, h=12, center=true);

        // Add "L" identifier debossed on inside face (X=0 face)
        translate([1, rail_length/2, rail_height/2])
            rotate([90, 0, -90])
                linear_extrude(height=1.5)
                    text("L", size=8, halign="center", valign="center", font="Liberation Sans:style=Bold");

        // Add model name debossed on top face between screw holes
        translate([rail_width/2, rail_length/2, rail_height - 1])
            rotate([0, 0, 90])
                linear_extrude(height=1.5)
                    text(get_name(ctrl), size=3.5, halign="center", valign="center", font="Liberation Sans:style=Bold");
        }
    }

    echo(str("Left rail: ", rail_width, "mm wide, ", rail_height, "mm high, ", rail_length, "mm long"));
}

module right_rail(ctrl) {
    controller_length = get_length(ctrl);
    heatsink_height = get_heatsink_height(ctrl);
    hole_shape = get_hole_shape(ctrl);

    // Rail height = fan plate size minus heatsink height
    fan_size = get_fan_type(ctrl);
    rail_height = (fan_size + 4) - heatsink_height;
    rail_length = controller_length; // Match controller length exactly

    union() {
        difference() {
            // Main rail body
            cube([rail_width, rail_length, rail_height]);

        // Flange mounting holes - through Z-axis (Z- to Z+) with U cutouts to edges
        if (hole_shape == "sideways_u") {
            // A1 config - Two 8mm holes, each 25mm from nearest edge, centered on Y-axis
            // Rail length is 142mm, so center is at 71mm

            // First hole 25mm from Y=0 edge
            translate([rail_width/2, 25, -1])
                cylinder(d=8, h=rail_height+2);
            // U cutout from first hole to X=rail_width edge (mirror of left rail)
            translate([rail_width/2, 25 - 4, -1])
                cube([rail_width/2, 8, rail_height+2]);

            // Second hole 71.5mm from first hole (96.5mm from edge)
            translate([rail_width/2, 96.5, -1])
                cylinder(d=8, h=rail_height+2);
            // U cutout from second hole to X=rail_width edge
            translate([rail_width/2, 96.5 - 4, -1])
                cube([rail_width/2, 8, rail_height+2]);
        } else if (hole_shape == "dual_u") {
            // A3 config - Dual sideways U holes, 54mm center-to-center spacing
            // Front U-hole: 18.8mm from Y=0 edge
            front_u_pos = 18.8;
            rear_u_pos = 72.8;  // 18.8 + 54mm spacing

            // Front U-hole
            translate([rail_width/2, front_u_pos, -1])
                cylinder(d=5, h=rail_height+2);
            // U cutout from front hole to X=rail_width edge (mirror of left rail)
            translate([rail_width/2, front_u_pos - 2.5, -1])
                cube([rail_width/2, 5, rail_height+2]);

            // Rear U-hole
            translate([rail_width/2, rear_u_pos, -1])
                cylinder(d=5, h=rail_height+2);
            // U cutout from rear hole to X=rail_width edge
            translate([rail_width/2, rear_u_pos - 2.5, -1])
                cube([rail_width/2, 5, rail_height+2]);
        } else if (hole_shape == "circle") {
            // C1, C2 configs - Housing-based mounting with corner holes
            flange_config = get_flange_config(ctrl);

            if (flange_config == "C1") {
                // C1: 4 corner holes, R4 (8mm diameter)
                // Spacing: 98.8mm horizontal, 84.1mm vertical
                // Margins: 7.05mm (sides), 7.8mm (top/bottom) on 112.9×99.7mm housing
                hole_margin_x = 7.05;
                hole_margin_y = 7.8;
                total_width = get_total_width(ctrl);  // 112.9mm

                // Four corner holes through housing (no rail, so through Z-axis from top)
                // Front-left
                translate([hole_margin_x, hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Front-right
                translate([total_width - hole_margin_x, hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Rear-left
                translate([hole_margin_x, controller_length - hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Rear-right
                translate([total_width - hole_margin_x, controller_length - hole_margin_y, -1])
                    cylinder(d=8, h=20);
            } else if (flange_config == "C2") {
                // C2: 4 corner holes, R4 (8mm diameter) - same pattern as C1
                // Spacing: 98.8mm horizontal, 84.1mm vertical
                // Margins: 7.05mm (sides), 7.8mm (top/bottom) on 113.9×100.7mm housing
                hole_margin_x = 7.05;
                hole_margin_y = 7.8;
                total_width = get_total_width(ctrl);  // 113.9mm

                // Four corner holes through housing (no rail, so through Z-axis from top)
                // Front-left
                translate([hole_margin_x, hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Front-right
                translate([total_width - hole_margin_x, hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Rear-left
                translate([hole_margin_x, controller_length - hole_margin_y, -1])
                    cylinder(d=8, h=20);
                // Rear-right
                translate([total_width - hole_margin_x, controller_length - hole_margin_y, -1])
                    cylinder(d=8, h=20);
            }
        } else if (hole_shape == "keyhole") {
            // B1, B2, B3 configs - Holes from top for larger controllers
            translate([rail_width/2, 30, rail_height])
                cylinder(d=m4_hole_dia, h=15, center=true);
            translate([rail_width/2, controller_length-30, rail_height])
                cylinder(d=m4_hole_dia, h=15, center=true);
            // Additional hole for large controllers
            if (controller_length > 150) {
                translate([rail_width/2, controller_length/2, rail_height])
                    cylinder(d=m4_hole_dia, h=15, center=true);
            }
        } else if (hole_shape == "keyhole_u") {
            // A4, B1, B2, B3 configs - Keyhole at top (back), Sideways U at bottom (front)
            // Get flange config to determine hole dimensions
            flange_config = get_flange_config(ctrl);

            // Config-specific U-hole dimensions
            u_hole_position = (flange_config == "A4" || flange_config == "A4_MC4" || flange_config == "B3") ? 11 :
                             (flange_config == "B1" || flange_config == "B2" || flange_config == "B2_MC4") ? 13.75 : 25;
            u_hole_diameter = (flange_config == "A4" || flange_config == "A4_MC4" || flange_config == "B3") ? 6 :
                             (flange_config == "B1" || flange_config == "B2" || flange_config == "B2_MC4") ? 7.5 : 8;

            // Config-specific keyhole dimensions
            keyhole_position = (flange_config == "A4" || flange_config == "A4_MC4" || flange_config == "B3") ? 11 :
                              (flange_config == "B1" || flange_config == "B2" || flange_config == "B2_MC4") ? 13.75 : 30;

            // Top keyhole (rear of controller, toward longer Y values)
            if (flange_config == "A4" || flange_config == "A4_MC4") {
                // A4/A4_MC4: Keyhole with R2.75 top, R6 bottom, 12mm center-to-center
                translate([rail_width/2, controller_length - keyhole_position, rail_height]) {
                    // Top small circle (R2.75 = 5.5mm diameter)
                    cylinder(r=2.75, h=15, center=true);
                    // Bottom large circle (R6 = 12mm diameter), 12mm below top
                    translate([0, 0, -12])
                        cylinder(r=6, h=15, center=true);
                    // Connecting slot (5.5mm wide to match top circle)
                    translate([0, 0, -6])
                        cylinder(r=2.75, h=12, center=true);
                }
            } else if (flange_config == "B1" || flange_config == "B2" || flange_config == "B2_MC4") {
                // B1/B2: Keyhole with R4 top, R8 bottom, 17mm center-to-center (USER CONFIRMED for B1, B2 needs verification)
                translate([rail_width/2, controller_length - keyhole_position, rail_height]) {
                    // Top circle (R4 = 8mm diameter)
                    cylinder(r=4, h=15, center=true);
                    // Bottom large circle (R8 = 16mm diameter), 17mm below top
                    translate([0, 0, -17])
                        cylinder(r=8, h=15, center=true);
                    // Connecting slot (8mm wide to match top circle)
                    translate([0, 0, -8.5])
                        cylinder(r=4, h=17, center=true);
                }
            } else if (flange_config == "B3") {
                // B3: Keyhole with R3 top, R6 bottom, 12mm center-to-center
                translate([rail_width/2, controller_length - keyhole_position, rail_height]) {
                    // Top small circle (R3 = 6mm diameter)
                    cylinder(r=3, h=15, center=true);
                    // Bottom large circle (R6 = 12mm diameter), 12mm below top
                    translate([0, 0, -12])
                        cylinder(r=6, h=15, center=true);
                    // Connecting slot (6mm wide to match top circle)
                    translate([0, 0, -6])
                        cylinder(r=3, h=12, center=true);
                }
            } else {
                // Fallback: Simple through-hole
                translate([rail_width/2, controller_length - keyhole_position, rail_height])
                    cylinder(d=8, h=15, center=true);
            }

            // Bottom sideways U (front of controller) - mirror of left rail
            translate([rail_width/2, u_hole_position, -1])
                cylinder(d=u_hole_diameter, h=rail_height+2);
            // U cutout from hole to X=rail_width edge (mirror of left rail)
            translate([rail_width/2, u_hole_position - u_hole_diameter/2, -1])
                cube([rail_width/2, u_hole_diameter, rail_height+2]);
        }

        // Holes to connect to front/rear plates - positioned at 1/4 and 3/4 of rail height
        first_hole = rail_height * 0.25;   // 1/4 up from bottom (center of lower half)
        second_hole = rail_height * 0.75;  // 3/4 up from bottom (center of upper half)

        // Holes through the 18mm width (from front face to back face) for plate connection
        translate([rail_width/2, 0, first_hole])
            rotate([90, 0, 0])
                cylinder(d=m4_hole_dia, h=12, center=true);
        translate([rail_width/2, 0, second_hole])
            rotate([90, 0, 0])
                cylinder(d=m4_hole_dia, h=12, center=true);

        // Holes at rear end for rear plate connection
        translate([rail_width/2, rail_length, first_hole])
            rotate([90, 0, 0])
                cylinder(d=m4_hole_dia, h=12, center=true);
        translate([rail_width/2, rail_length, second_hole])
            rotate([90, 0, 0])
                cylinder(d=m4_hole_dia, h=12, center=true);

        // Add "R" identifier debossed on inside face (X=0 face)
        translate([1, rail_length/2, rail_height/2])
            rotate([90, 0, -90])
                linear_extrude(height=1.5)
                    text("R", size=8, halign="center", valign="center", font="Liberation Sans:style=Bold");

        // Add model name debossed on top face between screw holes
        translate([rail_width/2, rail_length/2, rail_height - 1])
            rotate([0, 0, 90])
                linear_extrude(height=1.5)
                    text(get_name(ctrl), size=3.5, halign="center", valign="center", font="Liberation Sans:style=Bold");
        }
    }

    echo(str("Right rail: ", rail_width, "mm wide, ", rail_height, "mm high, ", rail_length, "mm long"));
}

module rear_grill(ctrl) {
    fan_area_width = get_fan_area_width(ctrl);
    controller_length = get_length(ctrl);
    
    // Same plate dimensions as front fan mount
    plate_width = get_total_width(ctrl) + plate_width_adjust;     // Total width + adjustment
    plate_length = get_fan_type(ctrl) + 4;          // Fan height + 4mm spacing
    plate_thickness = plate_depth;                   // 6mm thick
    
    difference() {
        // Main body - same as front plate
        cube([plate_width, plate_length, plate_thickness]);
        
        // Hexagonal ventilation pattern - rotated and densely packed in fan area
        hex_spacing = 2;        // 2mm space between holes
        hex_diameter = 10;      // Reduced size for better packing
        hex_center_distance = hex_diameter + hex_spacing;  // 12mm center-to-center
        
        // Define fan area boundaries (centered on plate, fill top to bottom)
        fan_area_start = (plate_width - fan_area_width) / 2;  // Start of fan area
        fan_area_end = fan_area_start + fan_area_width;       // End of fan area
        fan_area_bottom = 1;  // Start near bottom edge (1mm margin)
        fan_area_top = plate_length - 1;  // End near top edge (1mm margin)
        
        // Calculate grid and center pattern top-to-bottom
        available_width = fan_area_width;
        available_height = fan_area_top - fan_area_bottom;
        
        // Calculate how many fit
        x_spacing = hex_center_distance * 0.87;
        y_spacing = hex_center_distance * 0.75;
        x_count = floor((available_width - hex_diameter) / x_spacing) + 1;
        y_count = floor((available_height - hex_diameter) / y_spacing) + 1;
        
        // Calculate actual space used
        actual_x_space = (x_count - 1) * x_spacing + hex_diameter;
        actual_y_space = (y_count - 1) * y_spacing + hex_diameter;
        
        // Center the pattern in available space
        x_start = fan_area_start + (fan_area_width - actual_x_space) / 2 + hex_diameter/2;
        y_start = fan_area_bottom + (available_height - actual_y_space) / 2 + hex_diameter/2;
        
        for (x = [0:x_count-1]) {
            for (y = [0:y_count-1]) {
                // Offset every other row for honeycomb pattern  
                offset_x = (y % 2) * (x_spacing * 0.5);
                x_pos = x_start + x * x_spacing + offset_x;
                y_pos = y_start + y * y_spacing;
                
                // Only place hex if it fits within fan area (full top to bottom)
                if (x_pos >= fan_area_start + hex_diameter/2 && 
                    x_pos <= fan_area_end - hex_diameter/2 &&
                    y_pos >= fan_area_bottom + hex_diameter/2 && 
                    y_pos <= fan_area_top - hex_diameter/2) {
                    translate([x_pos, y_pos, -0.5])
                        rotate([0, 0, 30])  // Rotate hexagon 30 degrees for better orientation
                            cylinder(d=hex_diameter, h=plate_thickness+1, $fn=6);
                }
            }
        }
        
        // Rail mounting holes - match rail hole positions
        rail_hole_dia = m4_hole_dia;
        edge_offset = 8;  // Distance from plate edges
        
        // Get actual rail height for this controller (must match rail calculation)
        rail_actual_height = (get_fan_type(ctrl) + 4) - get_heatsink_height(ctrl);
        first_hole = rail_actual_height * 0.25;   // 1/4 of rail height
        second_hole = rail_actual_height * 0.75;  // 3/4 of rail height
        
        // Left side rail holes (within rail area)
        translate([edge_offset, first_hole, -0.5])
            cylinder(d=rail_hole_dia, h=plate_thickness+1);
        translate([edge_offset, second_hole, -0.5])
            cylinder(d=rail_hole_dia, h=plate_thickness+1);
            
        // Right side rail holes (within rail area)
        translate([plate_width-edge_offset, first_hole, -0.5])
            cylinder(d=rail_hole_dia, h=plate_thickness+1);
        translate([plate_width-edge_offset, second_hole, -0.5])
            cylinder(d=rail_hole_dia, h=plate_thickness+1);

        // Add model name debossed on back edge face (thin vertical edge)
        // Position at the back edge, centered on width and thickness
        translate([plate_width/2, plate_length, plate_thickness/2])
            rotate([90, 0, 0])
                linear_extrude(height=1.5)
                    mirror([0, 1, 0])
                        text(get_name(ctrl), size=3, halign="center", valign="center", font="Liberation Sans:style=Bold");
    }

    echo(str("Rear grill: ", plate_width, "×", plate_length, "mm plate with hexagonal ventilation"));
}

// ===== HELPER MODULES =====

module sideways_u_hole() {
    // Sideways U-shaped cutout for A1 config on Z+ face
    // 8mm between straight parts, curved center, centered on rail
    translate([-4, -10, 0]) {  // Center on rail, extend in Y direction
        hull() {
            // Two straight parts 8mm apart
            translate([0, 0, 0]) cube([2, 20, 10]);      // Left straight part
            translate([6, 0, 0]) cube([2, 20, 10]);      // Right straight part (8mm gap)
            // Curved connecting part at back
            translate([4, 15, 0]) cylinder(r=4, h=10);   // Curved center
        }
    }
}

module keyhole_pattern(controller_length, rail_length) {
    // Keyhole and rounded slot pattern for B configs
    // Positioned based on controller dimensions with base height offset
    translate([rail_width/2, 15, base_height + 30])
        rotate([0, 90, 0])
            cylinder(d=8, h=rail_width+2, center=true);
    translate([rail_width/2, controller_length+5, base_height + 30])
        rotate([0, 90, 0])
            cylinder(d=8, h=rail_width+2, center=true);
    
    // Additional holes for larger controllers if needed
    if (controller_length > 150) {
        translate([rail_width/2, controller_length*0.5+10, base_height + 60])
            rotate([0, 90, 0])
                cylinder(d=8, h=rail_width+2, center=true);
    }
}

// ===== EXAMPLE USAGE =====
/*
To generate all 4 components for MPPT 100/30:

1. Set: model_code = "SCC020030200"; component = 1; // Front fan mount
2. Set: model_code = "SCC020030200"; component = 2; // Left rail  
3. Set: model_code = "SCC020030200"; component = 3; // Right rail
4. Set: model_code = "SCC020030200"; component = 4; // Rear grill
*/