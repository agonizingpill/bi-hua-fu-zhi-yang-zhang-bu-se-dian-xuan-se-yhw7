from domain.proof_regions_api import router as proof_regions
from domain.dry_swatches_api import router as dry_swatches
from domain.shade_studies_api import router as shade_studies
from domain.patch_slots_api import router as patch_slots

routers = (proof_regions, dry_swatches, shade_studies, patch_slots,)
