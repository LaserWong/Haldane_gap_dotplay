"""Read-only exact model matching to explicitly historical project certificates.

No audit execution, proof promotion, numerical-result replacement or remote I/O.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from .model import Model

CATALOG_PATH = Path(__file__).parent/'catalog_data'/'uniform_spin1_0248.json'


def _match_uniform_spin1(model):
    g=model.geometry
    if g.get('type')!='lattice' or len(g.get('shape',[]))!=1:
        return False,'Requires the one-dimensional lattice model declaration'
    L=g['shape'][0]
    if L<2 or g.get('periodic') != [True]:
        return False,'Requires an untwisted periodic chain of length at least two'
    if g.get('bond_convention')!='positive_direction_multigraph':
        return False,'Requires the periodic multigraph convention, including both L=2 bonds'
    if len(model.spins2)!=L or any(s!=2 for s in model.spins2):
        return False,'Requires spin one at every site'
    expected=Counter(tuple(sorted((i,(i+1)%L))) for i in range(L))
    actual=Counter()
    for term in model.terms:
        if len(term)!=5 or term[0]!='exchange' or term[3]!=F(1) or term[4]!=F(1):
            return False,'Requires only unit isotropic bilinear exchange, with no perturbations or shifts'
        actual[tuple(sorted((term[1],term[2])))]+=1
    if actual!=expected:
        return False,'Exchange placement or multiplicity differs from the uniform periodic Hamiltonian'
    return True,'Exact model, unit normalization, periodic geometry and bond multiplicities match'


def _sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def inspect_catalog_artifacts(repository_root, catalog=None):
    """Check accessible raw dependencies. Changed prose is never a hash blocker."""
    catalog=catalog or json.loads(CATALOG_PATH.read_text())
    root=Path(repository_root).resolve()
    verified=[];missing=[];mismatched=[];unreadable=[]
    for relative,expected in catalog['raw_dependencies_sha256'].items():
        path=(root/relative).resolve()
        if not path.is_relative_to(root):
            unreadable.append({'path':relative,'reason':'Path resolves outside repository root'})
            continue
        if not path.is_file():
            missing.append(relative)
            continue
        try:
            actual=_sha256(path)
        except OSError as exc:
            unreadable.append({'path':relative,'reason':str(exc)})
            continue
        if actual==expected:
            verified.append(relative)
        else:
            mismatched.append({'path':relative,'expected_sha256':expected,'actual_sha256':actual})
    evidence_status=('RAW_IDENTITY_MISMATCH' if mismatched else
                     'ARTIFACTS_UNAVAILABLE' if missing or unreadable else
                     'LISTED_RAW_IDENTITIES_VERIFIED')
    return {'status':evidence_status,'verified_count':len(verified),'verified':verified,
            'missing_count':len(missing),'missing':missing,'mismatched':mismatched,
            'unreadable':unreadable,'documentation_hashes_checked':False,
            'scope':catalog['identity_scope'], 'mathematical_replay_performed':False}


def match_catalog(model, repository_root=None):
    """Return a separate historical match. Never modify a finite-size result.

    `model` is a validated Model or model specification, not the full request.
    `repository_root` is optional and used only for local read-only hash checks.
    All reported evidence paths are repository-relative.
    """
    base={'status':'NO_CATALOG_MATCH','freshly_independently_replayed':False,
          'new_uniform_family_claim':False,'computed_finite_bound_overridden':False}
    try:
        if not isinstance(model,Model):
            model=Model.from_dict(model)
        matches,reason=_match_uniform_spin1(model)
        if not matches:
            return {**base,'reason':reason}
    except (ValueError,TypeError,KeyError,AttributeError) as exc:
        return {**base,'status':'INVALID_INPUT','reason':str(exc)}
    catalog=json.loads(CATALOG_PATH.read_text())
    evidence=(inspect_catalog_artifacts(repository_root,catalog) if repository_root is not None else
              {'status':'NOT_INSPECTED','reason':'No local repository root supplied',
               'mathematical_replay_performed':False,'documentation_hashes_checked':False})
    return {**base,'status':'HISTORICAL_CERTIFICATE_MATCH','catalog_id':catalog['catalog_id'],
            'reason':reason, 'historical_claim':{
                'gap_lower':catalog['gap_lower'],'all_integer_L_at_least':2,
                'unique_ground_state':True,'bootstrap_initialization':34,
                'separately_certified_smaller_initialization':30,
                'smaller_initialization_gap':'179/10000',
                'normalization':'H=sum_i S_i dot S_(i+1), spin one, hbar=1, unit bilinear coupling',
                'boundary':'untwisted periodic with two adjacency terms at L=2',
                'evidence_level':'historically independently accepted, not newly replayed'},
            'proof_documents':catalog['proof_documents'],
            'result_artifact':catalog['review_path']+'/results.json',
            'source_manifest_sha256':catalog['source_manifest_sha256'],
            'artifact_inspection':evidence,
            'historical_resource_exception':'The direct L=25 resource-enforcement anomaly remains unresolved. Later guarded runs do not erase it.',
            'limitations':['Raw identity checks are not a fresh mathematical proof',
                           'The direct dependency list is not recursively complete replay closure',
                           'No perturbed, rescaled, open-boundary, twisted or different-spin model is covered',
                           'This record is separate from any user-computed finite-size bound']}
