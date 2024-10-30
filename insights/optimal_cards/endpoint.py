from database.auth.user import User
from insights.optimal_cards.milp_setup import setup_model
from insights.optimal_cards.r_matrix import compute_r_matrix
from insights.optimal_cards.solution_extraction import extract_solution
from insights.schemas import OptimalCardsAllocationRequest, OptimalCardsAllocationResponse, RMatrixDetails
from insights.utils import hamming_distance
from sqlalchemy.orm import Session


async def optimize_credit_card_selection_milp(db: Session, user: User, request: OptimalCardsAllocationRequest) -> OptimalCardsAllocationResponse:
    # Step 1: Compute the reward matrix
    rmatrix: RMatrixDetails = await compute_r_matrix(db=db, user=user, request=request)
    model, x, z, s_il = setup_model(request=request, rmatrix=rmatrix)
    
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
            s_il=s_il
        )
        
        # Don't send duplicate solutions
        if all(hamming_distance(solution, sol) >= 1 for sol in solutions):
            solutions.append(solution)
        
        if len(solutions) >= request.num_solutions:
            break
        
    return OptimalCardsAllocationResponse(
        timeframe=rmatrix.timeframe,
        solutions=solutions
    )
