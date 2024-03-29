from pyqpanda import circuit_layer
from pyqpanda import draw_qprog_text
from pyqpanda import draw_qprog_latex
from pyqpanda import fit_to_gbk
from pyqpanda import count_prog_info
from .matplotlib_draw import *


def draw_circuit_pic(prog, pic_name, scale = 0.7,verbose=False,fold = 30):
    layer_info = circuit_layer(prog)
    qcd = MatplotlibDrawer(
        qregs=layer_info[1], cregs=layer_info[2], ops=layer_info[0], scale = scale,fold = fold)
    qcd.draw(pic_name, verbose)


def draw_qprog(prog, output=None, scale=0.7, fold =30, filename=None, with_logo=False, line_length=100, NodeIter_first=None,
               NodeIter_second=None, console_encode_type='utf8'):
    """Draw a quantum circuit to different formats (set by output parameter):

    **text**: ASCII art TextDrawing that can be printed in the console.
    **text**: ASCII art TextDrawing that can be printed in the console.

    **pic**: images with color rendered purely in Python.

    **latex**: latex source code of circuit

    Args:
        prog : the quantum circuit to draw
        scale (float): scale of image to draw (shrink if < 1). Only used by the ``pic`` outputs.
        flod (int): x_max_size of image to draw. dOnly used by the ``pic`` outputs. Default is 30.
        filename (str): file path to save image to
        NodeIter_first: circuit printing start position.
        NodeIter_second: circuit printing end position.
        console_encode_type(str): Target console encoding type. 
            Mismatching of encoding types may result in character confusion, 'utf8' and 'gbk' are supported.
            Only used by the ``pic`` outputs.
        line_length (int): Sets the length of the lines generated by `text` output type.

    Returns: 
        no return

    """
    default_output = 'text'
    if output is None:
        output = default_output

    text_pic = 'null'
    if output == 'pic':
        if filename is None:
            filename = 'QCircuit_pic.jpg'
        draw_circuit_pic(prog,filename,scale,fold = fold)
    elif output == 'text':
        if filename is None:
            filename = ''
        if NodeIter_first is None and NodeIter_second is None:
            text_pic = draw_qprog_text(prog, line_length, filename)
        elif NodeIter_first is None:
            text_pic = draw_qprog_text(
                prog, line_length, filename, prog.begin(), NodeIter_second)
        elif NodeIter_second is None:
            text_pic = draw_qprog_text(
                prog, line_length, filename, NodeIter_first, prog.end())

        if console_encode_type == 'gbk':
            text_pic = fit_to_gbk(text_pic)

        # print(text_pic)
    elif output == 'latex':
        if filename is None:
            filename = 'QCircuit_latex.tex'
        if NodeIter_first is None and NodeIter_second is None:
            text_pic = draw_qprog_latex(
                prog, line_length, filename, with_logo)
        elif NodeIter_first is None:
            text_pic = draw_qprog_latex(
                prog, line_length, filename, with_logo, prog.begin(), NodeIter_second)
        elif NodeIter_second is None:
            text_pic = draw_qprog_latex(
                prog, line_length, filename, with_logo, NodeIter_first, prog.end())

    return text_pic

def show_prog_info_count(prog):

    info_count = count_prog_info(prog)

    labels_node = ['Single Gate Node', 'Double Gate Node', 'Multi Control Gate Node', 'Other Nodes']
    sizes_node = [info_count.single_gate_num, 
                  info_count.double_gate_num, 
                  info_count.multi_control_gate_num, 
                  info_count.node_num - info_count.single_gate_num - info_count.double_gate_num - info_count.multi_control_gate_num]

    labels_layer = ['Single Gate Layer', 'Double Gate Layer', 'Other Layers']
    sizes_layer = [info_count.single_gate_layer_num, info_count.double_gate_layer_num, info_count.layer_num - info_count.single_gate_layer_num - info_count.double_gate_layer_num]

    fig, axes = plt.subplots(nrows=2, figsize=(6, 8))
    plt.subplots_adjust(hspace=0.2)

    total_node_num = info_count.node_num
    wedges_node, texts_node, autotexts_node = axes[0].pie(sizes_node, labels=labels_node, autopct='%.1f%%', startangle=140, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
    axes[0].set_title(f'Total Nodes Distribution (Total Nodes: {total_node_num})', fontsize=14)
    axes[0].set_aspect('equal')

    for i, (label, size) in enumerate(zip(labels_node, sizes_node)):
        texts_node[i].set_text(f'{label} ({size})')

    total_layer_num = info_count.layer_num
    wedges_layer, texts_layer, autotexts_layer = axes[1].pie(sizes_layer, labels=labels_layer, autopct='%.1f%%', startangle=140, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
    axes[1].set_title(f'Total Layers Distribution (Total Layers: {total_layer_num})', fontsize=14)
    axes[1].set_aspect('equal')

    for i, (label, size) in enumerate(zip(labels_layer, sizes_layer)):
        texts_layer[i].set_text(f'{label} ({size})')

    plt.show()
    