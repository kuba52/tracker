#!/usr/bin/env wolframscript

scriptPath = ExpandFileName[First[$ScriptCommandLine]];
scriptName = Last[FileNameSplit[ scriptPath ]];

path = StringTrim[scriptPath, scriptName];
Print[path];

distanceToPlane = 100;
fov = 100Degree;
resolutionInPix = {1280,720};

planeWidth = Tan[fov/2]*distanceToPlane*2;
planeHigh = planeWidth * resolutionInPix[[2]]/resolutionInPix[[1]];
PaceOnPlane[{x_,y_}] :={ x/resolutionInPix[[1]]*planeHigh, y/resolutionInPix[[2]] planeWidth}


inFile = OpenRead[path<>"data.txt"];
outFile = OpenWrite[path<>"data2.txt"];
Close[outFile];

strem = ReadLine[inFile];
While[strem =!= EndOfFile,


Print[strem];
    vars = Read[StringToStream[strem], {Number,Number, Number}];
    pos = PaceOnPlane[{vars[[1]], vars[[2]]}] // N;



    outFile = OpenAppend[path<>"data2.txt"];
    WriteString[outFile, NumberForm[pos[[1]]], " ", NumberForm[pos[[2]]], " ", NumberForm[vars[[3]]], "\n" ];
    Close[outFile];
    strem = ReadLine[inFile];
]
Close[inFile];

(* ::Package:: *)

(* ::Input:: *)
(*(*camPos = {-3,3,3};*)*)
(*camPos = {0,0,0};*)
(*camRotation ={-Pi/4,-Pi/4} ;(*<xy, xz> *)*)
(*pointOnFish = {200,300};*)
(*pointPos = {1,1,1};*)
(*(*directionToPoint = { -Pi/4,-Pi/4};*)*)
(**)
(**)
(*pointOnScreen = {0,0};*)
(**)

(**)
(*iconHight = 10;*)
(*iconBaseWidth = Tan[fov/2]*iconHight*2;*)
(*iconBaseHigh = iconBaseWidth * resolutionInPix[[2]]/resolutionInPix[[1]];*)
(**)
(*fishEyeRExtra = 5;*)
(*fishEyeR = Sqrt[(iconHight+fishEyeRExtra)^2+(iconBaseWidth/2)^2+(iconBaseHigh/2)^2];*)
(*fishEyeStartPos  ={-fishEyeRExtra,0,0};*)
(*fishEyeMaxToSide = (iconBaseWidth/2)/fishEyeR;*)
(*fishEyeMaxToSideAngl = ArcSin[fishEyeMaxToSide];*)
(*fishEyeMaxToTop = (iconBaseHigh/2)/fishEyeR;*)
(*fishEyeMaxToTopAngl = ArcSin[fishEyeMaxToTop];*)
(*PlaceOnFish[{w_,h_}]:= Module[{sideAngl=(2w-resolutionInPix[[1]])/(resolutionInPix[[1]])*fishEyeMaxToSideAngl,*)
(*topAngl=(2h-resolutionInPix[[2]])/(resolutionInPix[[2]])*fishEyeMaxToTopAngl},*)
(*(RotationMatrix[topAngl,RotationMatrix[sideAngl,{0,0,1}] . {0,1,0}] . RotationMatrix[sideAngl,{0,0,1}] . {fishEyeR,0,0})+fishEyeStartPos]*)
(**)
(*intersectWPlane[v_,pV_,pP_]:=Module[{tVal= t /.Solve[(v t -pP)pV== {0,0,0},t][[1]] },Print[tVal//N];v* tVal]*)
(**)
(**)
(**)
(*rotate[g_, di_]:=Rotate[ *)
(*Rotate[ g   ,di[[1]],{0,0,1}],*)
(*di[[2]], RotationTransform[di[[1]],{0,0,1}][{0,-1,0}]]*)
(*rotate2[g_, di_]:=*)
(*Rotate[ g   ,di[[2]],{0,0,1}]*)
(*mountCamera[g_] :=Translate[*)
(*rotate[g, camRotation], camPos];*)
(*camIcon = Rotate[Translate[  Pyramid[{{0,0,0},{iconBaseHigh ,0,0},{iconBaseHigh,iconBaseWidth ,0},{0,iconBaseWidth ,0},{iconBaseHigh/2,iconBaseWidth/2,iconHight}}],{-iconBaseHigh/2,-iconBaseWidth/2,-iconHight}],90Degree,{0,-1,0}];*)
(*camIconInPos =mountCamera[camIcon];*)
(*camAxi = {Dashed,mountCamera[InfiniteLine[{0,0,0},{1,0,0} ]]};*)
(*(*lineToPoint = {Red, Dashed, Line[{ pointPos,camPos}]}*)*)
(**)
(*pointOnCamIconCor =  RotationTransform [90Degree,{0,-1,0}][*)
(*{pointOnScreen[[1]]/resolutionInPix[[1]]*iconBaseHigh, pointOnScreen[[2]]/resolutionInPix[[2]]iconBaseWidth,0}+{-iconBaseHigh/2,-iconBaseWidth/2,-iconHight}] ;*)
(*pointOnCamIcon = Point[pointOnCamIconCor];*)
(**)
(*plane = Rotate[Translate[Cuboid[*)
(*{0,0,0},{planeHigh,planeWidth,0}],*)
(*{-planeHigh/2,-planeWidth/2,-distanceToPlane}],90Degree,{0,-1,0}] ;*)
(*PaceOnPlane[{x_,y_}] :={ x/resolutionInPix[[1]]*planeHigh, y/resolutionInPix[[2]]planeWidth}*)
(*pointOnPlaneIconCor = RotationTransform [90Degree,{0,-1,0}][*)
(*{pointOnScreen[[1]]/resolutionInPix[[1]]*planeHigh, pointOnScreen[[2]]/resolutionInPix[[2]]planeWidth,0}+{-planeHigh/2,-planeWidth/2,-distanceToPlane}] ;*)
(*pointOnPlaneIcon = Point[pointOnPlaneIconCor];*)
(**)
(*pOnFish = PlaceOnFish[{1280,720/2}];*)
(*pOnIcon = intersectWPlane[pOnFish,{1,0,0},{iconHight,0,0}] //N;*)
(*Graphics3D[{{Opacity[.1],Sphere[fishEyeStartPos,fishEyeR]},Point[{pOnFish, pOnIcon }],{Opacity[.1],camIcon}(*,{Red,pointOnCamIcon ,pointOnPlaneIcon}, {Opacity[.1],plane}, {Dashed, Black, Line[{{0,0,0},pointOnPlaneIconCor}]}*)},  Axes->True, AxesLabel->{x,y,z}]*)
(*Graphics3D[{{Red, Opacity[.2],camIconInPos},{Black, Opacity[.2],Translate[rotate[camIcon, {-Pi/4,0}], camPos]}},  Axes->True, AxesLabel->{x,y,z}];*)
(**)
(*Graphics3D[{Point[{0,0,0}],{Red,Point[pointPos]},Point[camPos], camIconInPos ,camAxi}, Axes->True, AxesLabel->{x,y,z}];*)


(* ::Input:: *)
(*$ScriptCommandLine*)
(*data=Table[{RandomReal[i],RandomReal[i^10]},{i,0,100,0.1}];*)
(*outFile = OpenAppend["data3.txt"];*)
(*Export[outFile,data,"Table"]*)
(*Close[outFile]*)
(*$TemporaryDirectory*)


(* ::Input:: *)
(* = OpenRead["data.txt"];*)
(*While[true; *)
(*vars = ReadList[str, {Number, Number, Number}];*)
(*pos = PaceOnPlane[{vars[[1]], vars[[2]]}];*)
(*Export*)
(*]*)
(*Close[file];*)
(**)
