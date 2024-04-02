# local
import startai
import jax
from startai_tests.test_startai.helpers import handle_frontend_test
from startai.functional.frontends.jax._src.tree_util import tree_leaves, tree_map
import hypothesis.strategies as st


# --- Helpers --- #
# --------------- #


@st.composite
def _tree_dict_strategy(draw):
    return draw(tree_strategy())


# --- Main --- #
# ------------ #


def leaf_strategy():
    return st.lists(st.integers(1, 10)).map(startai.array)


# tree_leaves
@handle_frontend_test(
    fn_tree="jax._src.tree_util.tree_leaves",
    tree=_tree_dict_strategy(),
)
def test_jax_tree_leaves(
    *,
    tree,
    test_flags,
    fn_tree,
    frontend,
    on_device,
    backend_fw,
):
    startai.set_backend(backend_fw)
    # Apply the tree_leaves function to obtain the leaves of the tree
    result = tree_leaves(tree)

    # compute the expected result
    expected = jax.tree_util.tree_leaves(tree)

    # value test
    assert result == expected
    startai.previous_backend()


# tree_map
@handle_frontend_test(
    fn_tree="jax._src.tree_util.tree_map",
    tree=_tree_dict_strategy(),
)
def test_jax_tree_map(
    *,
    tree,
    test_flags,
    fn_tree,
    frontend,
    on_device,
    backend_fw,
):
    startai.set_backend(backend_fw)

    # Define a function to square each leaf node
    def square(x):
        if isinstance(x, startai.Array):
            return startai.square(x)
        else:
            return x**2

    # Apply the square function to the tree using tree_map
    result = tree_map(square, tree)

    # compute the expected result
    expected = startai.square(startai.Container(tree))

    assert startai.equal(startai.Container(result), expected)
    startai.previous_backend()


def tree_strategy(max_depth=2):
    if max_depth == 0:
        return leaf_strategy()
    else:
        return st.dictionaries(
            keys=st.one_of(
                *[
                    st.text(
                        alphabet=st.characters(min_codepoint=97, max_codepoint=122),
                        min_size=1,
                        max_size=1,
                    ).filter(lambda x: x not in used_keys)
                    for used_keys in [set()]
                ]
            ),
            values=st.one_of(leaf_strategy(), tree_strategy(max_depth - 1)),
            min_size=1,
            max_size=10,
        )
