import os
from agent.project_context import project_context

class Migrator:

    def __init__(self):
        self.root = project_context.project_root
        self.modules_root = os.path.join(self.root, "modules")
        self.legacy = project_context.legacy_dirs

    def scan_old_files(self):
        files = []
        for d in self.legacy:
            for r, dirs, fs in os.walk(d):
                for f in fs:
                    if f.endswith(".py") or f.endswith(".html"):
                        files.append(os.path.join(r, f))
        return files

    def classify_file(self, old_path):
        """
        FARM 专用分类（可换成通用模式）
        """
        p = old_path.lower()

        if "farm" not in p:
            return None

        # 根
        if "farm_home" in p or "farm_structure" in p or "farm_base" in p:
            return "domain_operations/farm_domain"

        # species
        if "barn" in p or "pen" in p or "buyer" in p or "category" in p:
            return "domain_operations/farm_domain/species"

        # timeline
        if "timeline" in p or "lineage" in p or "batch" in p:
            return "domain_operations/farm_domain/timeline"

        # event engine
        if "event" in p or "note" in p or "move" in p or "death" in p or "inbound" in p:
            return "domain_operations/farm_domain/event_engine"

        # analytics
        if "stats" in p or "api_sync" in p or "api.py" in p:
            return "domain_operations/farm_domain/analytics"

        # records
        if "code" in p or "sync" in p:
            return "domain_operations/farm_domain/records"

        # fallback → 放根域
        return "domain_operations/farm_domain"

    def build_move_plan(self):
        plan = []
        for f in self.scan_old_files():
            target = self.classify_file(f)
            if target:
                fname = os.path.basename(f)
                new_path = os.path.join(self.root, "modules", target, fname)
                plan.append({"old": f, "new": new_path})
        return plan

migrator = Migrator()
