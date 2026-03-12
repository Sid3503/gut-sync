"""
Test image upload integration to verify:
1. Graph compiles successfully without errors
2. State initialization works with image fields
3. Routing logic handles images correctly
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.getcwd()))

from src.agent.gutsync_agent.graph.graph import create_gutsync_graph
from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState

def test_graph_compilation():
    """Test that graph compiles successfully with image nodes."""
    print("=" * 60)
    print("TEST 1: Graph Compilation")
    print("=" * 60)
    
    try:
        graph = create_gutsync_graph()
        print("✅ Graph compiled successfully!")
        return True
    except Exception as e:
        print(f"❌ Graph compilation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_state_initialization():
    """Test that state can be initialized with all image fields."""
    print("\n" + "=" * 60)
    print("TEST 2: State Initialization with Images")
    print("=" * 60)
    
    try:
        state: GutSyncState = {
            "user_input": "I have a rash on my arm",
            "symptoms": [],
            "timing": None,
            "diet_changes": None,
            "medications": [],
            "symptom_patterns": [],
            "possible_root_causes": [],
            "severity": None,
            "relief_strategies": [],
            "red_flags": [],
            "report": None,
            # PDF State
            "pdf_uploaded": False,
            "pdf_file_path": None,
            "pdf_extracted_text": None,
            "pdf_medical_summary": None,
            "pdf_key_findings": None,
            # Image State (NEW)
            "images_uploaded": True,
            "image_file_paths": ["/test/image1.jpg", "/test/image2.jpg"],
            "image_count": 2,
            "image_descriptions": [],
            "image_visual_summary": None,
            "image_key_observations": [],
            "image_clinical_relevance": None
        }
        print("✅ State initialized successfully with image fields!")
        print(f"   - images_uploaded: {state['images_uploaded']}")
        print(f"   - image_count: {state['image_count']}")
        print(f"   - image_file_paths: {state['image_file_paths']}")
        return True
    except Exception as e:
        print(f"❌ State initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_routing_logic():
    """Test that routing works for different scenarios."""
    print("\n" + "=" * 60)
    print("TEST 3: Routing Logic")
    print("=" * 60)
    
    from src.agent.gutsync_agent.graph.router.pdf_router import route_for_pdf
    from src.agent.gutsync_agent.graph.router.image_router import route_for_images
    
    # Test 1: No PDF, No Images
    state1 = {"pdf_uploaded": False, "images_uploaded": False}
    result1 = route_for_pdf(state1)
    print(f"Scenario 1 (No PDF, No Images): {result1}")
    assert result1 == "symptom_analysis_node", f"Expected symptom_analysis_node, got {result1}"
    print("   ✅ Correct routing")
    
    # Test 2: PDF uploaded, No Images
    state2 = {"pdf_uploaded": True, "images_uploaded": False}
    result2 = route_for_pdf(state2)
    print(f"\nScenario 2 (PDF, No Images): {result2}")
    assert result2 == "pdf_analysis_node", f"Expected pdf_analysis_node, got {result2}"
    print("   ✅ Correct routing")
    
    # Test 3: No PDF, Images uploaded
    state3 = {"pdf_uploaded": False, "images_uploaded": True}
    result3 = route_for_pdf(state3)
    print(f"\nScenario 3 (No PDF, Images): {result3}")
    assert result3 == "image_analysis_node", f"Expected image_analysis_node, got {result3}"
    print("   ✅ Correct routing")
    
    # Test 4: Both PDF and Images
    state4 = {"pdf_uploaded": True, "images_uploaded": True, "image_file_paths": ["/test/img.jpg"]}
    result4_pdf = route_for_pdf(state4)
    print(f"\nScenario 4 (PDF + Images): PDF router -> {result4_pdf}")
    assert result4_pdf == "pdf_analysis_node", f"Expected pdf_analysis_node, got {result4_pdf}"
    
    # After PDF enrichment, check image router
    result4_img = route_for_images(state4)
    print(f"                             Image router -> {result4_img}")
    assert result4_img == "image_analysis_node", f"Expected image_analysis_node, got {result4_img}"
    print("   ✅ Correct routing for both")
    
    print("\n✅ All routing tests passed!")
    return True

def main():
    """Run all tests."""
    print("\n🧪 IMAGE UPLOAD INTEGRATION TESTS\n")
    
    results = []
    
    # Test 1: Graph Compilation
    results.append(("Graph Compilation", test_graph_compilation()))
    
    # Test 2: State Initialization
    results.append(("State Initialization", test_state_initialization()))
    
    # Test 3: Routing Logic
    results.append(("Routing Logic", test_routing_logic()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Test with actual image files using test_api_client.py")
        print("2. Verify GPT-4o-mini vision API integration")
        print("3. Review generated report with Visual Observations section")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    exit(main())
