/*
Point numbering convention:
    0xx: nozzle contour (converging and diverging), except parabolic profile
    1xx: temporary points
    2xx: parabolic profile spline
    3xx: stagnation reservoir and dump tank
Line numbering convention:
    0xx: nozzle contours, including parabolic profile splint
    1xx: stagnation resevoir and dump tank
Curve loops, surface convention:
    0xx: all
*/

R_t = 8e-3; // throat radius
theta_n = 15*Pi/180; // angle at point N
theta_i = 75*Pi/180; // angle at inlet section
epsilon = 5; // exit area to throat area ratio
R_e = R_t*Sqrt(epsilon); // exit radius
x_n = 0.382*R_t*Sin(theta_n); // coordinates of point N
y_n = R_t + 0.382*R_t*(1-Cos(theta_n));
x_i = -1.5*R_t*Sin(theta_i); // coordinates of inlet section
y_i = R_t + 1.5*R_t*(1-Cos(theta_i));

a = 1.729e2; // coefficients for parabola
b = 9.298e-1;
c = -1.81e-2;

// converging section (circular arc)
Point(100) = {0, 2.5*R_t, 0}; // arc center
Point(1) = {x_i, y_i, 0};
Point(2) = {0, R_t, 0};
Point(3) = {-1.5*R_t, 0, 0};
Point(4) = {0, 0, 0};
Circle(1) = {1, 100, 2};
Line(2) = {3,4};
Line(3) = {3,1};
Line(4) = {4,2};
Curve Loop(1) = {2,4,-1,-3};

// circular arc after throat
Point(101) = {0, 1.382*R_t, 0}; // arc center
Point(5) = {x_n, y_n, 0};
Point(6) = {x_n, 0, 0};
Circle(5) = {2, 101, 5};
Line(6) = {4,6};
Line(7) = {6,5};
Curve Loop(2) = {6,7,-5,-4};

// parabolic portion
/// define points on the parabolic section
n_parabola = 25; // number of points to be defined on parabola
For i In {1:n_parabola}
    y = y_n + (R_e-y_n)*i/n_parabola;
    Point(200+i-1) = {a*y^2 + b*y + c, y, 0};
EndFor
BSpline(8) = {5,200:200+n_parabola-1};
x_e = a*R_e^2 + b*R_e + c; // x coordinate of exit section
Point(7) = {x_e, 0, 0};
Line(9) = {6,7};
Line(10) = {7,200+n_parabola-1};
Curve Loop(3) = {9,10,-8,-7};

// stagnation reservoir
Point(300) = {2*x_i, 2*y_i, 0};
Point(301) = {2*x_i, y_i, 0};
Point(302) = {2*x_i, 0, 0};
Point(303) = {x_i, 2*y_i, 0};
Line(100) = {300,303};
Line(101) = {301,1};
Line(102) = {302,3};
Line(104) = {302,301};
Line(105) = {301,300};
Line(106) = {1,303};
Curve Loop(4) = {101,106,-100,-105};
Curve Loop(5) = {102,3,-101,-104};

// dumping tank
Point(304) = {1.25*x_e, 0, 0};
Point(305) = {1.25*x_e, R_e, 0};
Point(306) = {1.25*x_e, 2*R_e, 0};
Point(307) = {x_e, 2*R_e, 0};
Line(107) = {7,304};
Line(108) = {200+n_parabola-1,305};
Line(109) = {307,306};
Line(110) = {304,305};
Line(111) = {305,306};
Line(112) = {200+n_parabola-1,307};
Curve Loop(6) = {107,110,-108,-10};
Curve Loop(7) = {108,111,-109,-112};



// plane surfaces, transfinite and recombine; extrude and physical entities
Transfinite Curve{1} = 10 Using Progression 0.9;
Transfinite Curve{2} = 10;
Transfinite Curve{5,6} = 3;
Transfinite Curve{8,9} = 20;
Transfinite Curve{3,4,7,10,104,110} = 10;
Transfinite Curve{100:102} = 5;
Transfinite Curve{105,106} = 5;
Transfinite Curve{107:109} = 5;
Transfinite Curve{111,112} = 5;
For i In {1:7}
    Plane Surface(i) = {i};
    Transfinite Surface{i};
    Recombine Surface{i};
    out~{i}[] = Extrude{
        {1,0,0},
        {0,0,0},
        15*Pi/180
    }{
        Surface{i};
        Layers{1};
        Recombine;
    };
EndFor
Physical Volume("volume", 1) = {};
Physical Surface("back", 1) = {};
Physical Surface("front", 2) = {};
Physical Surface("inflow", 3) = {};
Physical Surface("outflow", 4) = {};
Physical Surface("wall", 5) = {};
For i In {1:7}
    Physical Volume(1) += {out~{i}[1]};
    Physical Surface(1) += {i};
    Physical Surface(2) += {out~{i}[0]};
EndFor
For i In {1:3}
    Physical Surface(5) += {out~{i}[3]};
EndFor
Physical Surface(3) += {out_5[4], out_4[3], out_4[4], out_4[5]};
Physical Surface(4) += {out_6[2], out_7[3], out_7[4], out_7[5]};

