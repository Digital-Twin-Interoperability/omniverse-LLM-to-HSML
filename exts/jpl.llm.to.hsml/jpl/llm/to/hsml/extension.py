import omni.ext
import omni.usd
from pxr import UsdGeom

class MySelectionPrinter(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[MySelectionPrinter] Starting up!")
        # Get the current selection context from Omniverse USD
        self._selection = omni.usd.get_context().get_selection()
        # Register the selection callback
        self._selection_callback = self._selection.add_callback(self._on_selection_changed)
        print("Selection callback added.")

    def on_shutdown(self):
        print("[MySelectionPrinter] Shutting down!")
        # Unregister the callback to clean up properly
        if self._selection_callback:
            self._selection.remove_callback(self._selection_callback)
            self._selection_callback = None

    def _on_selection_changed(self, selection_paths):
        # Get the current stage
        stage = omni.usd.get_context().get_stage()
        if not stage:
            print("No stage loaded.")
            return

        # Iterate through all selected prim paths
        for prim_path in selection_paths:
            prim = stage.GetPrimAtPath(prim_path)
            if prim:
                # Use UsdGeom.Xformable to access transform operations
                xformable = UsdGeom.Xformable(prim)
                ops = xformable.GetOrderedXformOps()
                translation = None
                # Look for a translate operation in the ordered XformOps
                for op in ops:
                    if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                        translation = op.Get()
                        break

                # If no translate op is found, assume the origin
                if translation is None:
                    translation = (0.0, 0.0, 0.0)

                print(f"Selected Prim: {prim_path} - Coordinates: {translation}")
