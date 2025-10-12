# Medical Visualization Blueprint Template

## Blueprint Information
- **Blueprint Name**: [BP_Name]
- **Blueprint Type**: [Actor / Pawn / Character / Component]
- **Medical Domain**: [Anatomy / Physiology / Pathology / Diagnostic]
- **Complexity**: [Simple / Intermediate / Advanced]
- **UE Version**: 5.3+

---

## Overview
[Brief description of what this blueprint visualizes and its educational purpose]

---

## Blueprint Class Structure

### Parent Class
```
Parent: Actor (or appropriate base class)
```

### Components Hierarchy
```
BP_[Name]
├── DefaultSceneRoot (SceneComponent)
├── StaticMesh_Main (StaticMeshComponent)
│   └── Materials: M_Medical_[Type]
├── SkeletalMesh_[Organ] (SkeletalMeshComponent) [if animated]
├── ParticleSystem_[Effect] (ParticleSystemComponent)
├── Widget_Info (WidgetComponent)
├── Audio_Ambient (AudioComponent)
└── Collision_Interaction (BoxComponent)
```

---

## Variables

### Public Variables (Editable)
```cpp
// Visual Settings
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Medical Visualization")
float VisualizationScale = 1.0;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Medical Visualization")
bool bShowLabels = true;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Medical Visualization")
EMedicalDetailLevel DetailLevel = EMedicalDetailLevel::High;

// Interaction Settings
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Interaction")
bool bIsInteractive = true;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Interaction")
float RotationSpeed = 50.0;

// Animation Settings
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
bool bAutoPlay = false;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
float AnimationSpeed = 1.0;
```

### Private Variables (Internal Use)
```cpp
// State Management
UPROPERTY(BlueprintReadOnly, Category = "State")
bool bIsHighlighted = false;

UPROPERTY(BlueprintReadOnly, Category = "State")
int32 CurrentLayerIndex = 0;

UPROPERTY(BlueprintReadOnly, Category = "State")
TArray<UMaterialInstanceDynamic*> DynamicMaterials;
```

---

## Functions

### Construction Script
```
┌─────────────────────────────────────┐
│    Construction Script              │
├─────────────────────────────────────┤
│ 1. Create Dynamic Material Instance │
│ 2. Setup Components                 │
│ 3. Initialize Labels                │
│ 4. Configure Collision              │
└─────────────────────────────────────┘
```

**Implementation Notes**:
- Create dynamic material instances for runtime changes
- Position and configure widget components
- Set initial visibility states
- Configure interaction collision volumes

### Event Graph - Core Events

#### Event BeginPlay
```
Event BeginPlay
    └─> Initialize Medical Data
        └─> Setup Interaction Handlers
            └─> Start Animation (if AutoPlay)
                └─> Register with Game Manager
```

#### Event Tick
```
Event Tick
    └─> [Optional] Update Animation State
        └─> [Optional] Update Dynamic Parameters
            └─> [Optional] Update UI Elements
```

**Note**: Minimize Tick usage for performance

---

## Custom Functions

### Function: Initialize Medical Data
```
Input: None
Output: None

Flow:
1. Load medical metadata
2. Initialize anatomical labels
3. Setup material parameters
4. Configure initial state
```

### Function: Toggle Anatomical Layer
```
Input: LayerIndex (int32)
Output: bool (Success)

Flow:
1. Validate layer index
2. Update material opacity
3. Toggle component visibility
4. Update UI state
5. Trigger sound effect
```

### Function: Highlight Region
```
Input: RegionName (FName), bHighlight (bool)
Output: None

Flow:
1. Find target component by name
2. Get dynamic material instance
3. Set emission color parameter
4. Play highlight animation
5. Show/hide region label
```

### Function: Play Medical Animation
```
Input: AnimationName (FName)
Output: None

Flow:
1. Validate animation exists
2. Stop current animation
3. Play target animation
4. Update UI to show animation controls
5. Broadcast animation started event
```

### Function: Show Information Panel
```
Input: InfoType (EMedicalInfoType)
Output: None

Flow:
1. Get relevant medical information
2. Update widget content
3. Animate panel in
4. Focus camera on relevant area
```

### Function: Reset Visualization
```
Input: None
Output: None

Flow:
1. Reset all material parameters
2. Reset component transforms
3. Stop all animations
4. Clear all highlights
5. Hide information panels
```

---

## Events and Delegates

### Custom Events

#### Event: OnInteractionStarted
```
Custom Event: OnInteractionStarted
Params: InteractionType (EMedicalInteractionType)

Implementation:
- Update interaction state
- Change cursor icon
- Enable interaction feedback
```

#### Event: OnLayerChanged
```
Custom Event: OnLayerChanged
Params: OldLayer (int32), NewLayer (int32)

Implementation:
- Fade out old layer
- Fade in new layer
- Update navigation UI
```

### Delegates (for communication with other blueprints)

```cpp
// Declare Event Dispatcher
UPROPERTY(BlueprintAssignable, Category = "Medical Events")
FOnMedicalVisualizationChanged OnVisualizationChanged;

UPROPERTY(BlueprintAssignable, Category = "Medical Events")
FOnRegionSelected OnRegionSelected;
```

---

## Material Parameters

### Dynamic Parameters
```
Parameter Name              | Type   | Default | Purpose
---------------------------|--------|---------|---------------------------
EmissionIntensity          | Scalar | 0.0     | Highlight intensity
LayerOpacity              | Scalar | 1.0     | Layer visibility
ColorTint                 | Vector | (1,1,1) | Region color coding
PulseRate                 | Scalar | 1.0     | Animation pulse speed
DetailLevel               | Scalar | 1.0     | LOD control
```

### Setting Parameters (Blueprint)
```
Material Instance (Dynamic)
    └─> Set Scalar Parameter Value
        Name: "EmissionIntensity"
        Value: [0.0 - 5.0]
```

---

## Interaction System

### Mouse Interaction
```
Event: OnBeginMouseOver
    └─> Highlight Region
        └─> Show Tooltip
            └─> Change Cursor

Event: OnEndMouseOver
    └─> Remove Highlight
        └─> Hide Tooltip
            └─> Reset Cursor

Event: OnClicked
    └─> Select Region
        └─> Show Information Panel
            └─> Play Click Sound
```

### VR Interaction
```
Event: OnVRControllerHover
    └─> Highlight at HitLocation
        └─> Vibrate Controller (light)

Event: OnVRControllerTrigger
    └─> Select at HitLocation
        └─> Vibrate Controller (strong)
        └─> Show Information Panel
```

---

## Animation Setup

### Timeline: Fade Layer
```
Timeline: TL_FadeLayer
Duration: 0.5 seconds
Curve: Alpha (0.0 to 1.0, EaseInOut)

Update Pin:
    └─> Set Material Parameter (LayerOpacity)
        Value: Alpha

Finished Pin:
    └─> OnLayerChanged Event
```

### Timeline: Pulse Effect
```
Timeline: TL_Pulse
Duration: 2.0 seconds
Loop: True
Curve: Pulse (0.0 to 1.0 to 0.0, Sinusoidal)

Update Pin:
    └─> Set Material Parameter (EmissionIntensity)
        Value: Pulse * 2.0
```

---

## Widget Integration

### Widget Component Setup
```
Widget Class: WBP_MedicalLabel
Screen Space: World
Pivot: (0.5, 1.0)
Draw Size: (200, 50)
```

### Widget Interface Functions
```
Function: UpdateLabelText
    Input: NewText (FText)
    Implementation: Call widget function to update text

Function: SetLabelVisibility
    Input: bVisible (bool)
    Implementation: Toggle widget visibility
```

---

## Performance Considerations

### LOD Configuration
```
LOD 0 (High Detail): < 500 units
- Full mesh complexity
- High-res textures
- All interactive elements

LOD 1 (Medium Detail): 500-1500 units
- Reduced mesh complexity (50%)
- Mid-res textures
- Main interactive elements only

LOD 2 (Low Detail): > 1500 units
- Simplified mesh (25% original)
- Low-res textures
- No interactive elements
```

### Optimization Checklist
- [ ] Use LODs for complex meshes
- [ ] Minimize tick usage (use timers instead)
- [ ] Cache component references
- [ ] Use object pooling for repeated elements
- [ ] Optimize collision complexity
- [ ] Use texture compression
- [ ] Implement distance culling

---

## Medical Accuracy Validation

### Required Checks
- [ ] Anatomical proportions verified
- [ ] Medical terminology accurate
- [ ] Color coding follows medical standards
- [ ] Spatial relationships correct
- [ ] Pathology representation accurate
- [ ] Reviewed by medical professional

### Medical References
- Reference Source: [Textbook/Database]
- Validation Date: [Date]
- Reviewer: [Name, Credentials]

---

## Testing Checklist

### Functionality Tests
- [ ] All layers toggle correctly
- [ ] Highlights work on all regions
- [ ] Animations play smoothly
- [ ] Information panels display correctly
- [ ] Reset function returns to initial state
- [ ] VR interaction works (if applicable)

### Performance Tests
- [ ] FPS maintains target on minimum spec
- [ ] Memory usage within acceptable range
- [ ] No memory leaks during extended use
- [ ] LOD transitions are smooth

### Compatibility Tests
- [ ] Works on target platforms
- [ ] VR compatibility verified
- [ ] Mobile compatibility (if required)
- [ ] Web build compatibility (if required)

---

## Integration Requirements

### Required Interfaces
```cpp
BPI_MedicalVisualization
- GetMedicalMetadata()
- SetVisualizationMode()
- GetCurrentState()
```

### Required Game Manager Functions
```cpp
- RegisterMedicalActor()
- UnregisterMedicalActor()
- GetMedicalData(AssetID)
```

---

## Documentation Links
- [Link to detailed medical reference]
- [Link to interaction guidelines]
- [Link to material setup guide]
- [Link to animation guidelines]

---

## Version History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial blueprint design |

## Notes
[Additional implementation notes, known issues, or future improvements]
