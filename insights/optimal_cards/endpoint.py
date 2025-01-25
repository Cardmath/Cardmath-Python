from database.auth.user import User, Onboarding
from insights.optimal_cards.milp_setup import setup_model
from insights.optimal_cards.r_matrix import compute_r_matrix
from insights.optimal_cards.solution_extraction import extract_solution
from insights.schemas import OptimalCardsAllocationRequest, OptimalCardsAllocationResponse, RMatrixDetails
from insights.utils import hamming_distance
from insights.optimal_cards.justify import generate_justification_from_solution
from insights.heavyhitters import get_mock_heavy_hitters_response, only_has_mock_txns
from sqlalchemy.orm import Session
from typing import Union

async def optimize_credit_card_selection_milp(db: Session, user: Union[User, Onboarding], request: OptimalCardsAllocationRequest) -> OptimalCardsAllocationResponse:

    if isinstance(user, User) and only_has_mock_txns(user=user):
        request.heavy_hitters_response_override = get_mock_heavy_hitters_response(db=db, user_id=user.id)

    rmatrix: RMatrixDetails = await compute_r_matrix(db=db, user=user, request=request)
    
    if not rmatrix:
        return
    
    model, x, z, s_il, credit_reduction = setup_model(request=request, rmatrix=rmatrix)
    
    solutions = []
    for i in range(request.num_solutions):
        model.optimize()
        if model.getStatus() not in ["optimal", "feasible"]:
            break

        solution = extract_solution(
            model=model,
            request=request,
            rmatrix=rmatrix,
            x=x,
            z=z,
            s_il=s_il, 
            credit_reduction=credit_reduction
        )
        
        # Don't send duplicate solutions
        if all(hamming_distance(solution, sol) >= 1 for sol in solutions):
            solutions.append(solution)
        
        if len(solutions) >= request.num_solutions:
            break

    justification = generate_justification_from_solution(solution=solutions[0])
    solutions[0].justification = justification
    return OptimalCardsAllocationResponse(
        timeframe=rmatrix.timeframe,
        solutions=solutions
    )
